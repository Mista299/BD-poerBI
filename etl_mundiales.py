"""
ETL - Mundiales de Fútbol Masculino para Power BI
Fuente: https://github.com/jfjelstul/worldcup

Genera esquema estrella en ./powerbi_data/:
  Dimensiones: DimTournament, DimTeam, DimPlayer, DimDate, DimStage
  Hechos:      FactMatches, FactGoals, FactTeamTournament
  Auxiliares:  TopScorers, Bookings, Diccionario_de_Datos.csv
"""

import os, io
import requests
import pandas as pd
import numpy as np

OUTPUT_DIR = "powerbi_data"
GITHUB_RAW = "https://raw.githubusercontent.com/jfjelstul/worldcup/master/data-csv/"

os.makedirs(OUTPUT_DIR, exist_ok=True)

RAW_FILES = [
    "tournaments.csv",
    "matches.csv",
    "goals.csv",
    "teams.csv",
    "players.csv",
    "squads.csv",
    "team_appearances.csv",
    "player_appearances.csv",
    "tournament_stages.csv",
    "host_countries.csv",
    "stadiums.csv",
    "groups.csv",
    "group_standings.csv",
    "tournament_standings.csv",
    "bookings.csv",
    "confederations.csv",
    "penalty_kicks.csv",
    "substitutions.csv",
]

# IDs de los mundiales MASCULINOS (filtro global aplicado a todas las tablas)
MENS_TOURNAMENT_IDS = None  # se llena tras descargar tournaments.csv

CONFEDERATION_MAP = {
    "UEFA":     "Europa",
    "CONMEBOL": "Sudamérica",
    "CONCACAF": "Norteamérica/Centroamérica/Caribe",
    "CAF":      "África",
    "AFC":      "Asia",
    "OFC":      "Oceanía",
}

# ─────────────────────────────────────────────────────────────────────────────
# 1. DESCARGA
# ─────────────────────────────────────────────────────────────────────────────
print("=" * 62)
print("PASO 1: Descargando datos desde GitHub...")
print("=" * 62)

raw = {}
for fname in RAW_FILES:
    url = GITHUB_RAW + fname
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        raw[fname] = pd.read_csv(io.StringIO(r.text))
        print(f"  OK  {fname:45s}  {len(raw[fname]):>5} filas")
    except Exception as e:
        print(f"  ERR {fname}: {e}")

# ─────────────────────────────────────────────────────────────────────────────
# FILTRO: solo mundiales masculinos
# ─────────────────────────────────────────────────────────────────────────────
MENS_TOURNAMENT_IDS = set(
    raw["tournaments.csv"]
    .loc[raw["tournaments.csv"]["tournament_name"].str.contains("Men's", na=False), "tournament_id"]
)
print(f"\nMundiales masculinos encontrados: {len(MENS_TOURNAMENT_IDS)}")
for tid in sorted(MENS_TOURNAMENT_IDS):
    print(f"  {tid}")

def filter_mens(df, col="tournament_id"):
    if col in df.columns:
        return df[df[col].isin(MENS_TOURNAMENT_IDS)].copy()
    return df

# ─────────────────────────────────────────────────────────────────────────────
# 2. DimTournament
# ─────────────────────────────────────────────────────────────────────────────
print("\nPASO 2: DimTournament...")

tours = filter_mens(raw["tournaments.csv"])
standings = filter_mens(raw["tournament_standings.csv"])

# Subcampeón y tercer lugar (tournaments.csv ya trae winner/host_country)
runner_up = (
    standings[standings["position"] == 2][["tournament_id","team_name"]]
    .rename(columns={"team_name": "RunnerUp"})
)
third_place = (
    standings[standings["position"] == 3][["tournament_id","team_name"]]
    .rename(columns={"team_name": "ThirdPlace"})
)

dim_tournament = (
    tours
    .merge(runner_up,   on="tournament_id", how="left")
    .merge(third_place, on="tournament_id", how="left")
    .rename(columns={
        "tournament_id":   "TournamentID",
        "tournament_name": "TournamentName",
        "year":            "Year",
        "start_date":      "StartDate",
        "end_date":        "EndDate",
        "host_country":    "HostCountry",
        "winner":          "Champion",
        "count_teams":     "NumTeams",
    })
)

dim_tournament = dim_tournament[[
    "TournamentID","TournamentName","Year","StartDate","EndDate",
    "HostCountry","NumTeams","Champion","RunnerUp","ThirdPlace"
]].drop_duplicates(subset="TournamentID")

dim_tournament.to_csv(f"{OUTPUT_DIR}/DimTournament.csv", index=False)
print(f"  -> DimTournament.csv  ({len(dim_tournament)} filas)")

# ─────────────────────────────────────────────────────────────────────────────
# 3. DimTeam
# ─────────────────────────────────────────────────────────────────────────────
print("\nPASO 3: DimTeam...")

teams = raw["teams.csv"].copy()

# teams.csv ya incluye confederation_code y confederation_name directamente
teams["Continent"] = teams["confederation_code"].map(CONFEDERATION_MAP).fillna("Desconocido")

dim_team = teams.rename(columns={
    "team_id":              "TeamID",
    "team_name":            "TeamName",
    "team_code":            "TeamCode",
    "federation_name":      "FederationName",
    "region_name":          "Region",
    "confederation_code":   "ConfederationCode",
    "confederation_name":   "ConfederationName",
})

keep = ["TeamID","TeamName","TeamCode","ConfederationCode","ConfederationName","Continent","Region","FederationName"]
dim_team = dim_team[[c for c in keep if c in dim_team.columns]].drop_duplicates(subset="TeamID")

dim_team.to_csv(f"{OUTPUT_DIR}/DimTeam.csv", index=False)
print(f"  -> DimTeam.csv  ({len(dim_team)} filas)")

# ─────────────────────────────────────────────────────────────────────────────
# 4. DimPlayer
# ─────────────────────────────────────────────────────────────────────────────
print("\nPASO 4: DimPlayer...")

squads  = filter_mens(raw["squads.csv"])
players = raw["players.csv"].copy()
# Solo jugadores que participaron en mundiales masculinos
mens_player_ids = set(squads["player_id"].unique())
players = players[players["player_id"].isin(mens_player_ids)].copy()

# Equipo principal por jugador
main_team = (
    squads.groupby("player_id")["team_name"]
    .agg(lambda x: x.value_counts().index[0])
    .reset_index()
    .rename(columns={"team_name": "MainTeam"})
)

dim_player = players.merge(main_team, on="player_id", how="left")

def clean_name_part(s):
    s = str(s).strip() if pd.notna(s) else ""
    return "" if s.lower() in ("not applicable", "n/a", "nan") else s

dim_player["FullName"] = (
    dim_player.apply(
        lambda r: (clean_name_part(r["given_name"]) + " " +
                   clean_name_part(r["family_name"])).strip(),
        axis=1
    )
)

def get_position(row):
    positions = []
    if row.get("goal_keeper"): positions.append("Portero")
    if row.get("defender"):    positions.append("Defensa")
    if row.get("midfielder"):  positions.append("Mediocampista")
    if row.get("forward"):     positions.append("Delantero")
    return " / ".join(positions) if positions else "Desconocido"

dim_player["Position"] = dim_player.apply(get_position, axis=1)

dim_player = dim_player.rename(columns={
    "player_id":        "PlayerID",
    "family_name":      "FamilyName",
    "given_name":       "GivenName",
    "birth_date":       "BirthDate",
    "count_tournaments":"TournamentsPlayed",
})

keep = ["PlayerID","FullName","FamilyName","GivenName","BirthDate",
        "Position","MainTeam","TournamentsPlayed"]
dim_player = dim_player[[c for c in keep if c in dim_player.columns]].drop_duplicates(subset="PlayerID")

dim_player.to_csv(f"{OUTPUT_DIR}/DimPlayer.csv", index=False)
print(f"  -> DimPlayer.csv  ({len(dim_player)} filas)")

# ─────────────────────────────────────────────────────────────────────────────
# 5. DimDate
# ─────────────────────────────────────────────────────────────────────────────
print("\nPASO 5: DimDate...")

matches_raw = raw["matches.csv"].copy()
dates = pd.to_datetime(matches_raw["match_date"].dropna().unique())

dim_date = (
    pd.DataFrame({"FullDate": dates})
    .sort_values("FullDate")
    .reset_index(drop=True)
)
dim_date["DateKey"]   = dim_date["FullDate"].dt.strftime("%Y%m%d").astype(int)
dim_date["Year"]      = dim_date["FullDate"].dt.year
dim_date["Month"]     = dim_date["FullDate"].dt.month
dim_date["MonthName"] = dim_date["FullDate"].dt.strftime("%B")
dim_date["Day"]       = dim_date["FullDate"].dt.day
dim_date["DayOfWeek"] = dim_date["FullDate"].dt.day_name()
dim_date["Quarter"]   = "Q" + dim_date["FullDate"].dt.quarter.astype(str)
dim_date["Decade"]    = (dim_date["Year"] // 10 * 10).astype(str) + "s"

dim_date.to_csv(f"{OUTPUT_DIR}/DimDate.csv", index=False)
print(f"  -> DimDate.csv  ({len(dim_date)} filas)")

# ─────────────────────────────────────────────────────────────────────────────
# 6. DimStage
# ─────────────────────────────────────────────────────────────────────────────
print("\nPASO 6: DimStage...")

STAGE_ORDER = {
    "first round": 1, "group stage": 1,
    "second group stage": 2,
    "round of 16": 3,
    "quarter-finals": 4,
    "semi-finals": 5,
    "third-place match": 6,
    "final": 7,
}

stages_src = raw["tournament_stages.csv"].copy()

dim_stage = (
    stages_src
    .drop_duplicates(subset=["stage_name"])
    .copy()
    .rename(columns={
        "stage_id":   "StageID",
        "stage_name": "StageName",
    })
)

dim_stage["StageOrder"] = (
    dim_stage["StageName"].str.lower()
    .map(STAGE_ORDER)
    .fillna(99)
    .astype(int)
)

dim_stage["IsKnockout"] = dim_stage["StageName"].str.lower().apply(
    lambda s: "No" if any(k in s for k in ["group", "first round"]) else "Sí"
)

keep = ["StageID","StageName","StageOrder","IsKnockout"]
dim_stage = dim_stage[[c for c in keep if c in dim_stage.columns]]

dim_stage.to_csv(f"{OUTPUT_DIR}/DimStage.csv", index=False)
print(f"  -> DimStage.csv  ({len(dim_stage)} filas)")

# ─────────────────────────────────────────────────────────────────────────────
# 7. FactMatches
# ─────────────────────────────────────────────────────────────────────────────
print("\nPASO 7: FactMatches...")

matches = filter_mens(matches_raw)

matches["match_date"] = pd.to_datetime(matches["match_date"], errors="coerce")
matches["DateKey"] = matches["match_date"].dt.strftime("%Y%m%d")
matches["DateKey"] = pd.to_numeric(matches["DateKey"], errors="coerce")

matches["TotalGoals"] = (
    pd.to_numeric(matches["home_team_score"], errors="coerce").fillna(0) +
    pd.to_numeric(matches["away_team_score"], errors="coerce").fillna(0)
).astype(int)

def match_result(row):
    try:
        if row["home_team_win"]: return "Local"
        if row["away_team_win"]: return "Visitante"
        return "Empate"
    except:
        return None

matches["MatchResult"] = matches.apply(match_result, axis=1)

# WinnerTeamID
def winner_id(row):
    try:
        if row["home_team_win"]: return row["home_team_id"]
        if row["away_team_win"]: return row["away_team_id"]
        return None
    except:
        return None

matches["WinnerTeamID"] = matches.apply(winner_id, axis=1)

fact_matches = matches.rename(columns={
    "match_id":                "MatchID",
    "tournament_id":           "TournamentID",
    "stage_name":              "StageName",
    "group_name":              "GroupName",
    "match_date":              "MatchDate",
    "match_time":              "MatchTime",
    "home_team_id":            "HomeTeamID",
    "home_team_name":          "HomeTeamName",
    "away_team_id":            "AwayTeamID",
    "away_team_name":          "AwayTeamName",
    "home_team_score":         "HomeGoals",
    "away_team_score":         "AwayGoals",
    "extra_time":              "WentToExtraTime",
    "penalty_shootout":        "WentToPenalties",
    "stadium_name":            "StadiumName",
    "city_name":               "City",
    "country_name":            "MatchCountry",
    "knockout_stage":          "IsKnockout",
    "group_stage":             "IsGroupStage",
})

keep = [
    "MatchID","TournamentID","StageName","GroupName","MatchDate","DateKey",
    "HomeTeamID","HomeTeamName","AwayTeamID","AwayTeamName",
    "HomeGoals","AwayGoals","TotalGoals","MatchResult","WinnerTeamID",
    "WentToExtraTime","WentToPenalties","IsKnockout","IsGroupStage",
    "StadiumName","City","MatchCountry",
]
fact_matches = fact_matches[[c for c in keep if c in fact_matches.columns]]
fact_matches = fact_matches.drop_duplicates(subset="MatchID")

fact_matches.to_csv(f"{OUTPUT_DIR}/FactMatches.csv", index=False)
print(f"  -> FactMatches.csv  ({len(fact_matches)} filas)")

# ─────────────────────────────────────────────────────────────────────────────
# 8. FactGoals
# ─────────────────────────────────────────────────────────────────────────────
print("\nPASO 8: FactGoals...")

goals = filter_mens(raw["goals.csv"])

# Nombre completo del goleador
goals["PlayerName"] = goals.apply(
    lambda r: (clean_name_part(r["given_name"]) + " " +
               clean_name_part(r["family_name"])).strip(),
    axis=1
)

def goal_type(row):
    if str(row.get("own_goal", "")).lower() in ["true", "1"]: return "Autogol"
    if str(row.get("penalty",  "")).lower() in ["true", "1"]: return "Penal"
    return "Gol normal"

goals["GoalType"] = goals.apply(goal_type, axis=1)

fact_goals = goals.rename(columns={
    "goal_id":       "GoalID",
    "match_id":      "MatchID",
    "tournament_id": "TournamentID",
    "team_id":       "TeamID",
    "team_name":     "TeamName",
    "player_id":     "PlayerID",
    "shirt_number":  "ShirtNumber",
    "minute_label":  "Minute",
    "match_period":  "Period",
    "stage_name":    "StageName",
    "match_date":    "MatchDate",
    "own_goal":      "IsOwnGoal",
    "penalty":       "IsPenalty",
})

keep = [
    "GoalID","MatchID","TournamentID","TeamID","TeamName",
    "PlayerID","PlayerName","ShirtNumber","Minute","Period",
    "GoalType","IsOwnGoal","IsPenalty","StageName","MatchDate",
]
fact_goals = fact_goals[[c for c in keep if c in fact_goals.columns]]
fact_goals = fact_goals.drop_duplicates(subset="GoalID")

fact_goals.to_csv(f"{OUTPUT_DIR}/FactGoals.csv", index=False)
print(f"  -> FactGoals.csv  ({len(fact_goals)} filas)")

# ─────────────────────────────────────────────────────────────────────────────
# 9. FactTeamTournament
# ─────────────────────────────────────────────────────────────────────────────
print("\nPASO 9: FactTeamTournament...")

team_app = filter_mens(raw["team_appearances.csv"])

agg = (
    team_app
    .groupby(["tournament_id","team_id","team_name"])
    .agg(
        MatchesPlayed  = ("match_id",          "nunique"),
        Wins           = ("win",               "sum"),
        Draws          = ("draw",              "sum"),
        Losses         = ("lose",              "sum"),
        GoalsFor       = ("goals_for",         "sum"),
        GoalsAgainst   = ("goals_against",     "sum"),
        ExtraTimeGames = ("extra_time",        "sum"),
        PenaltyGames   = ("penalty_shootout",  "sum"),
    )
    .reset_index()
)

final_standing = (
    standings[standings["position"].notna()]
    [["tournament_id","team_id","position"]]
    .rename(columns={"position": "FinalPosition"})
)

agg = agg.merge(final_standing, on=["tournament_id","team_id"], how="left")

agg["GoalDifference"] = agg["GoalsFor"] - agg["GoalsAgainst"]
agg["Points"] = agg["Wins"] * 3 + agg["Draws"]
agg["WinPct"] = (
    (agg["Wins"] / agg["MatchesPlayed"].replace(0, np.nan)) * 100
).round(1)

fact_team_tournament = agg.rename(columns={
    "tournament_id": "TournamentID",
    "team_id":       "TeamID",
    "team_name":     "TeamName",
})

fact_team_tournament.to_csv(f"{OUTPUT_DIR}/FactTeamTournament.csv", index=False)
print(f"  -> FactTeamTournament.csv  ({len(fact_team_tournament)} filas)")

# ─────────────────────────────────────────────────────────────────────────────
# 10. TopScorers (tabla auxiliar para página Goleadores)
# ─────────────────────────────────────────────────────────────────────────────
print("\nPASO 10: TopScorers...")

regular_goals = fact_goals[
    fact_goals["IsOwnGoal"].astype(str).str.lower().isin(["false", "0", "nan", ""])
].copy()

top_scorers = (
    regular_goals
    .groupby(["PlayerID","PlayerName","TeamName"])
    .agg(
        TotalGoals        = ("GoalID",       "count"),
        TournamentsScored = ("TournamentID", "nunique"),
        MatchesScored     = ("MatchID",      "nunique"),
    )
    .reset_index()
    .sort_values("TotalGoals", ascending=False)
    .reset_index(drop=True)
)
top_scorers["RankGlobal"] = (
    top_scorers["TotalGoals"].rank(method="min", ascending=False).astype(int)
)

top_scorers.to_csv(f"{OUTPUT_DIR}/TopScorers.csv", index=False)
print(f"  -> TopScorers.csv  ({len(top_scorers)} filas)")

# ─────────────────────────────────────────────────────────────────────────────
# 11. Bookings (tarjetas)
# ─────────────────────────────────────────────────────────────────────────────
print("\nPASO 11: Bookings...")

bookings = filter_mens(raw["bookings.csv"])
bookings["PlayerName"] = bookings.apply(
    lambda r: (clean_name_part(r.get("given_name","")) + " " +
               clean_name_part(r.get("family_name",""))).strip(),
    axis=1
)

bookings_out = bookings.rename(columns={
    "booking_id":    "BookingID",
    "match_id":      "MatchID",
    "tournament_id": "TournamentID",
    "team_id":       "TeamID",
    "team_name":     "TeamName",
    "player_id":     "PlayerID",
    "minute_label":  "Minute",
    "match_period":  "Period",
    "yellow_card":   "YellowCard",
    "red_card":      "RedCard",
    "second_yellow_card": "SecondYellow",
    "stage_name":    "StageName",
})

bookings_out.to_csv(f"{OUTPUT_DIR}/Bookings.csv", index=False)
print(f"  -> Bookings.csv  ({len(bookings_out)} filas)")

# ─────────────────────────────────────────────────────────────────────────────
# 12. Diccionario de datos
# ─────────────────────────────────────────────────────────────────────────────
print("\nPASO 12: Diccionario de datos...")

DICT = {
    "DimTournament": [
        ("TournamentID",  "TEXT",    "Identificador único del torneo (ej: WC-1930)"),
        ("TournamentName","TEXT",    "Nombre oficial del torneo"),
        ("Year",          "INTEGER", "Año de celebración"),
        ("StartDate",     "DATE",    "Fecha de inicio"),
        ("EndDate",       "DATE",    "Fecha de finalización"),
        ("HostCountry",   "TEXT",    "País(es) sede"),
        ("NumTeams",      "INTEGER", "Cantidad de selecciones participantes"),
        ("Champion",      "TEXT",    "Selección campeona"),
        ("RunnerUp",      "TEXT",    "Selección subcampeona"),
        ("ThirdPlace",    "TEXT",    "Tercer lugar"),
    ],
    "DimTeam": [
        ("TeamID",           "TEXT", "Identificador único de la selección"),
        ("TeamName",         "TEXT", "Nombre completo"),
        ("TeamCode",         "TEXT", "Código de 3 letras (BRA, ARG, etc.)"),
        ("ConfederationCode","TEXT", "Confederación (UEFA, CONMEBOL, etc.)"),
        ("ConfederationName","TEXT", "Nombre de la confederación"),
        ("Continent",        "TEXT", "Continente en español"),
        ("Region",           "TEXT", "Región geográfica"),
        ("FederationName",   "TEXT", "Federación nacional"),
    ],
    "DimPlayer": [
        ("PlayerID",          "TEXT",    "Identificador único del jugador"),
        ("FullName",          "TEXT",    "Nombre completo"),
        ("FamilyName",        "TEXT",    "Apellido"),
        ("GivenName",         "TEXT",    "Nombre de pila"),
        ("BirthDate",         "DATE",    "Fecha de nacimiento"),
        ("Position",          "TEXT",    "Posición (Portero/Defensa/Mediocampista/Delantero)"),
        ("MainTeam",          "TEXT",    "Selección principal"),
        ("TournamentsPlayed", "INTEGER", "Mundiales en los que participó"),
    ],
    "DimDate": [
        ("FullDate",  "DATE",    "Fecha completa"),
        ("DateKey",   "INTEGER", "Clave numérica YYYYMMDD para relaciones"),
        ("Year",      "INTEGER", "Año"),
        ("Month",     "INTEGER", "Mes numérico"),
        ("MonthName", "TEXT",    "Nombre del mes"),
        ("Day",       "INTEGER", "Día del mes"),
        ("DayOfWeek", "TEXT",    "Día de la semana"),
        ("Quarter",   "TEXT",    "Trimestre Q1-Q4"),
        ("Decade",    "TEXT",    "Década (1970s, 1980s, etc.)"),
    ],
    "DimStage": [
        ("StageID",    "TEXT",    "Identificador de fase"),
        ("StageName",  "TEXT",    "Nombre de la fase"),
        ("StageOrder", "INTEGER", "Orden lógico (1=grupos, 7=final)"),
        ("IsKnockout", "TEXT",    "¿Es eliminatoria? (Sí/No)"),
    ],
    "FactMatches": [
        ("MatchID",         "TEXT",    "Identificador único del partido"),
        ("TournamentID",    "TEXT",    "FK → DimTournament"),
        ("StageName",       "TEXT",    "FK → DimStage (por nombre)"),
        ("GroupName",       "TEXT",    "Nombre del grupo si aplica"),
        ("MatchDate",       "DATE",    "Fecha del partido"),
        ("DateKey",         "INTEGER", "FK → DimDate"),
        ("HomeTeamID",      "TEXT",    "FK → DimTeam (local)"),
        ("HomeTeamName",    "TEXT",    "Nombre equipo local"),
        ("AwayTeamID",      "TEXT",    "FK → DimTeam (visitante)"),
        ("AwayTeamName",    "TEXT",    "Nombre equipo visitante"),
        ("HomeGoals",       "INTEGER", "Goles del equipo local"),
        ("AwayGoals",       "INTEGER", "Goles del equipo visitante"),
        ("TotalGoals",      "INTEGER", "Total goles del partido"),
        ("MatchResult",     "TEXT",    "Local / Visitante / Empate"),
        ("WinnerTeamID",    "TEXT",    "FK → DimTeam (ganador)"),
        ("WentToExtraTime", "BOOLEAN", "¿Hubo prórroga?"),
        ("WentToPenalties", "BOOLEAN", "¿Hubo penales?"),
        ("IsKnockout",      "BOOLEAN", "¿Es fase eliminatoria?"),
        ("IsGroupStage",    "BOOLEAN", "¿Es fase de grupos?"),
        ("StadiumName",     "TEXT",    "Estadio"),
        ("City",            "TEXT",    "Ciudad"),
        ("MatchCountry",    "TEXT",    "País donde se jugó"),
    ],
    "FactGoals": [
        ("GoalID",      "TEXT",    "Identificador único del gol"),
        ("MatchID",     "TEXT",    "FK → FactMatches"),
        ("TournamentID","TEXT",    "FK → DimTournament"),
        ("TeamID",      "TEXT",    "FK → DimTeam"),
        ("TeamName",    "TEXT",    "Equipo que anotó"),
        ("PlayerID",    "TEXT",    "FK → DimPlayer"),
        ("PlayerName",  "TEXT",    "Nombre del goleador"),
        ("ShirtNumber", "INTEGER", "Número de camiseta"),
        ("Minute",      "TEXT",    "Minuto del gol"),
        ("Period",      "TEXT",    "Período (1H, 2H, ET1, ET2)"),
        ("GoalType",    "TEXT",    "Gol normal / Penal / Autogol"),
        ("IsOwnGoal",   "BOOLEAN", "¿Es autogol?"),
        ("IsPenalty",   "BOOLEAN", "¿Es penal?"),
        ("StageName",   "TEXT",    "Fase del torneo"),
        ("MatchDate",   "DATE",    "Fecha del partido"),
    ],
    "FactTeamTournament": [
        ("TournamentID",   "TEXT",    "FK → DimTournament"),
        ("TeamID",         "TEXT",    "FK → DimTeam"),
        ("TeamName",       "TEXT",    "Selección"),
        ("MatchesPlayed",  "INTEGER", "Partidos jugados"),
        ("Wins",           "INTEGER", "Victorias"),
        ("Draws",          "INTEGER", "Empates"),
        ("Losses",         "INTEGER", "Derrotas"),
        ("GoalsFor",       "INTEGER", "Goles a favor"),
        ("GoalsAgainst",   "INTEGER", "Goles en contra"),
        ("GoalDifference", "INTEGER", "Diferencia de gol"),
        ("Points",         "INTEGER", "Puntos (W×3 + D×1)"),
        ("WinPct",         "FLOAT",   "% de victorias"),
        ("ExtraTimeGames", "INTEGER", "Partidos que fueron a prórroga"),
        ("PenaltyGames",   "INTEGER", "Partidos que fueron a penales"),
        ("FinalPosition",  "INTEGER", "Posición final en el torneo"),
    ],
    "TopScorers": [
        ("PlayerID",          "TEXT",    "FK → DimPlayer"),
        ("PlayerName",        "TEXT",    "Nombre del goleador"),
        ("TeamName",          "TEXT",    "Selección"),
        ("TotalGoals",        "INTEGER", "Goles totales en mundiales (sin autogoles)"),
        ("TournamentsScored", "INTEGER", "Mundiales en los que anotó"),
        ("MatchesScored",     "INTEGER", "Partidos en los que anotó"),
        ("RankGlobal",        "INTEGER", "Ranking histórico"),
    ],
}

with open(f"{OUTPUT_DIR}/Diccionario_de_Datos.csv", "w", encoding="utf-8") as fh:
    fh.write("Tabla,Campo,Tipo,Descripcion\n")
    for table, fields in DICT.items():
        for field, dtype, desc in fields:
            fh.write(f"{table},{field},{dtype},{desc}\n")

print(f"  -> Diccionario_de_Datos.csv")

# ─────────────────────────────────────────────────────────────────────────────
# 13. VALIDACIONES
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 62)
print("VALIDACIONES")
print("=" * 62)

print("\n-- Mundiales por año y campeón --")
print(
    dim_tournament[["Year","Champion","HostCountry","NumTeams"]]
    .sort_values("Year")
    .to_string(index=False)
)

print("\n-- Títulos por selección --")
champs = dim_tournament["Champion"].value_counts().reset_index()
champs.columns = ["Seleccion","Titulos"]
print(champs.to_string(index=False))

print("\n-- Top 15 goleadores históricos --")
print(
    top_scorers[["RankGlobal","PlayerName","TeamName","TotalGoals"]]
    .head(15)
    .to_string(index=False)
)

print("\n-- Goles totales por torneo --")
goals_by_tour = (
    fact_matches
    .merge(dim_tournament[["TournamentID","Year"]], on="TournamentID", how="left")
    .groupby("Year")
    .agg(TotalGoals=("TotalGoals","sum"), Matches=("MatchID","count"))
    .assign(AvgGoalsPerMatch=lambda d: (d["TotalGoals"]/d["Matches"]).round(2))
    .sort_index()
)
print(goals_by_tour.to_string())

print("\n-- Partidos con más goles --")
top_matches = (
    fact_matches
    .nlargest(10, "TotalGoals")
    [["MatchID","HomeTeamName","HomeGoals","AwayGoals","AwayTeamName","StageName","MatchDate"]]
)
print(top_matches.to_string(index=False))

# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 62)
print("ETL COMPLETADO")
print(f"Archivos generados en: ./{OUTPUT_DIR}/")
print("=" * 62)
for f in sorted(os.listdir(OUTPUT_DIR)):
    kb = os.path.getsize(f"{OUTPUT_DIR}/{f}") // 1024
    print(f"  {f:<40s}  {kb:>4} KB")
