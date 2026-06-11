# Fuente de datos principal

**Título**: World Cup Database  
**Autor**: Joshua Fjelstul  
**Año**: 2024  
**Repositorio**: https://github.com/jfjelstul/worldcup  
**Fecha de consulta**: Junio 2026  
**Licencia**: MIT  

## Descripción

Repositorio de GitHub que contiene datos históricos completos de la Copa Mundial de Fútbol masculina, desde Uruguay 1930 hasta Catar 2022 (22 ediciones).

## Archivos disponibles

El repositorio contiene 18 archivos CSV en el directorio `data-csv/`:

| Archivo | Contenido | Registros |
|---------|-----------|-----------|
| tournaments.csv | Ediciones del torneo | 22 |
| matches.csv | Partidos disputados | 964 |
| goals.csv | Goles anotados | 2,720 |
| teams.csv | Selecciones nacionales | ~200 |
| players.csv | Jugadores | ~5,000 |
| squads.csv | Convocatorias por torneo | ~10,000 |
| team_appearances.csv | Apariciones de equipos por torneo | ~450 |
| player_appearances.csv | Apariciones de jugadores por torneo | ~15,000 |
| tournament_stages.csv | Fases del torneo | 8 |
| host_countries.csv | Países sede | 22 |
| stadiums.csv | Estadios | ~200 |
| groups.csv | Grupos | ~100 |
| group_standings.csv | Clasificación de grupos | ~400 |
| tournament_standings.csv | Clasificación final | ~450 |
| bookings.csv | Tarjetas (amarillas/rojas) | ~3,000 |
| confederations.csv | Confederaciones | 6 |
| penalty_kicks.csv | Penales en definición | ~200 |
| substitutions.csv | Sustituciones | ~5,000 |

## Metodología de validación del autor

Joshua Fjelstul documenta que los datos fueron validados contra:

1. **FIFA.com** — Archivo oficial de torneos, campeones y sedes
2. **RSSSF** (Rec.Sport.Soccer Statistics Foundation) — Estadísticas históricas detalladas
3. **Transfermarkt** — Datos de jugadores, goles y rankings
4. **Wikipedia** — Información complementaria de ediciones específicas

## Uso en este proyecto

- Se descargaron los 18 archivos CSV desde el repositorio
- Se aplicó filtro global para conservar solo torneos masculinos
- Se construyó esquema estrella con 5 dimensiones y 3 tablas de hechos
- Se generaron tablas auxiliares (TopScorers, Bookings)
- Se creó diccionario de datos automático

## Nota sobre actualizaciones

El repositorio se mantiene activo. Los datos de Catar 2022 fueron incorporados en la última versión disponible al momento de la consulta (junio 2026).
