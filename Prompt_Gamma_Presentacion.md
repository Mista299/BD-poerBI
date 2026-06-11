# Prompt para Gamma AI - Presentación Mundiales de Fútbol

## Instrucciones para copiar y pegar en Gamma AI

---

**Crea una presentación universitaria profesional sobre "Historia Analítica de los Mundiales de Fútbol Masculino" para un proyecto de Power BI en la materia de Bases de Datos.**

### Contexto del Proyecto

Este es un proyecto académico que analiza datos históricos de la Copa Mundial de Fútbol masculina desde 1930 hasta 2022 (22 ediciones). El objetivo es demostrar cómo se construyó un dashboard interactivo en Power BI utilizando datos reales, un modelo de datos en esquema estrella, y medidas DAX para responder preguntas analíticas concretas.

### Especificaciones de Diseño

**Estilo visual:**
- Diseño moderno y minimalista
- Paleta de colores: Azul oscuro (#1a365d), dorado/amarillo (#f6e05e), blanco, gris claro
- Tipografía: Sans-serif moderna (Montserrat, Poppins o similar)
- Mucho espacio en blanco
- Iconos e ilustraciones扁平 (flat design)
- Gráficos y visualizaciones de datos integrados
- Fotografías de alta calidad de mundiales cuando sea relevante
- Evitar diseños corporativos aburridos o plantillas genéricas

**Estructura:**
- 15 diapositivas máximo
- Formato widescreen (16:9)
- Transiciones suaves entre secciones

---

### Contenido por Diapositiva

**Diapositiva 1: Portada**
- Título principal: "Historia Analítica de los Mundiales de Fútbol"
- Subtítulo: "Proyecto de Analítica en Power BI"
- Información: "Bases de Datos | 2026-1"
- Imagen de fondo: Estadio de fútbol o trofeo de la Copa Mundial
- Diseño: Impactante, con imagen de fondo oscurecida y texto blanco

**Diapositiva 2: El Problema**
- Título: "¿Por qué analizar los Mundiales?"
- Contexto visual: Infografía con números grandes
  - 22 ediciones desde 1930
  - 964 partidos disputados
  - 2,720 goles anotados
- Pregunta central: "¿Cómo convertir datos históricos en información útil?"
- Diseño: Números grandes y destacados, iconos deportivos

**Diapositiva 3: Objetivos**
- Título: "Objetivo del Proyecto"
- Objetivo general en tarjeta destacada: "Diseñar un dashboard interactivo en Power BI que permita explorar la historia de los Mundiales masculinos de fútbol"
- 3 objetivos específicos con iconos:
  - 📊 Analizar 22 ediciones del torneo
  - 🏆 Identificar campeones y goleadores
  - 📈 Visualizar evolución histórica
- Diseño: Tarjetas con iconos, layout de 3 columnas

**Diapositiva 4: Fuente de Datos**
- Título: "Fuente de Datos"
- Logo de GitHub destacado
- Nombre: "World Cup Database - Joshua Fjelstul"
- Características en lista visual:
  - Repositorio público en GitHub
  - 18 archivos CSV con datos históricos
  - Validado contra FIFA.com y RSSSF
  - Licencia MIT - Uso académico
- URL: github.com/jfjelstul/worldcup
- Diseño: Card con información de la fuente, estilo técnico pero limpio

**Diapositiva 5: Proceso ETL**
- Título: "Proceso ETL (Extract, Transform, Load)"
- Diagrama de flujo visual con 3 pasos:
  1. **Extract** - Descarga 18 CSV desde GitHub
  2. **Transform** - Limpieza, filtro y transformación con Python/Pandas
  3. **Load** - Carga en esquema estrella para Power BI
- Tecnologías: Python + Pandas + Power BI (logos)
- Diseño: Diagrama de flujo horizontal con flechas, círculos numerados

**Diapositiva 6: Modelo de Datos**
- Título: "Modelo de Datos: Esquema Estrella"
- Diagrama visual del esquema estrella:
  - Centro: FactMatches (964 partidos)
  - Alrededor: DimTournament, DimTeam, DimPlayer, DimDate, DimStage
- Leyenda: "5 Dimensiones + 3 Tablas de Hechos + 2 Auxiliares"
- Diseño: Diagrama de estrella real con líneas conectoras, colores diferenciados para dimensiones (azul) y hechos (dorado)

**Diapositiva 7: Dashboard - Página Ejecutiva**
- Título: "Dashboard: Vista Ejecutiva"
- 4 tarjetas KPI grandes:
  - 22 Mundiales
  - 964 Partidos
  - 2,720 Goles
  - 2.82 Promedio goles/partido
- Descripción: "Vista panorámica con KPIs globales, mapa de sedes y evolución temporal"
- Espacio para captura de pantalla del dashboard
- Diseño: Tarjetas KPI estilo dashboard moderno, números grandes

**Diapositiva 8: Dashboard - Campeones**
- Título: "Dashboard: Campeones Históricos"
- Gráfico de barras horizontal:
  - Brasil: 5 títulos
  - Italia: 4 títulos
  - Alemania: 4 títulos
  - Argentina: 3 títulos
- Insight: "Brasil domina con 5 títulos y 7 finales disputadas"
- Diseño: Gráfico de barras limpio, colores por país, animación sugerida

**Diapositiva 9: Dashboard - Goleadores**
- Título: "Dashboard: Máximos Goleadores"
- Ranking visual Top 5:
  1. Miroslav Klose (Alemania) - 16 goles
  2. Ronaldo (Brasil) - 15 goles
  3. Gerd Müller (Alemania Occ.) - 14 goles
  4. Lionel Messi (Argentina) - 13 goles
  5. Just Fontaine (Francia) - 13 goles
- Diseño: Lista con medallas/oro-plata-bronce, barras de progreso para goles

**Diapositiva 10: Hallazgos Clave (1/2)**
- Título: "Hallazgos Clave"
- 4 tarjetas con hallazgos:
  -  **Brasil domina**: 5 títulos, 79 victorias (69.3% efectividad)
  - ⚽ **Suiza 1954**: 5.38 goles/partido (récord histórico)
  - 📈 **Evolución**: De 18 partidos (1930) a 64 (1998-2022)
  - 🎯 **Klose**: 16 goles en 4 mundiales (récord vigente)
- Diseño: Grid de 2x2 tarjetas con iconos, colores de acento

**Diapositiva 11: Hallazgos Clave (2/2)**
- Título: "Más Hallazgos"
- Hallazgo principal: "🌍 Europa y Sudamérica dominan"
  - 16 de 22 ediciones en estos continentes
- Gráfico de barras: Distribución de sedes
  - Europa: 11 ediciones
  - Sudamérica: 5 ediciones
  - Otros: 6 ediciones
- Dato destacado: "💡 66.5% de los goles se anotan en fase de grupos"
- Diseño: Gráfico de barras horizontal con colores por continente

**Diapositiva 12: Validación de Datos**
- Título: "Validación de Datos"
- Fuentes de validación (4 logos/cards):
  - FIFA.com
  - StatBunker
  - Transfermarkt
  - RSSSF
- Resultados con checkmarks verdes:
  - ✓ 22 campeones verificados
  - ✓ Top 10 goleadores coinciden
  - ✓ 22 sedes confirmadas
  - ✓ Partidos destacados validados
- Diseño: Layout de 2 columnas, logos de fuentes, lista de verificación

**Diapositiva 13: Limitaciones y Mejoras**
- Título: "Limitaciones y Mejoras Futuras"
- 2 columnas:
  - **Limitaciones** (fondo gris claro):
    - Datos de jugadores incompletos
    - Formato histórico variable
    - Consolidación de selecciones
    - Validación limitada de métricas avanzadas
  - **Mejoras** (fondo verde claro):
    - Incorporar métricas avanzadas
    - Integrar tabla de tarjetas
    - Análisis predictivo
    - Comparación masculino/femenino
- Diseño: Split screen, iconos de advertencia vs flechas hacia arriba

**Diapositiva 14: Entregables**
- Título: "Entregables del Proyecto"
- Lista visual con iconos:
  - 📊 Reporte Power BI (.pbix)
  - 📁 Dataset limpio (11 CSV)
  -  Diccionario de datos (.docx)
  - ✓ Documento de validación
  -  Metodología de datos (.docx)
- Diseño: Lista con iconos grandes, tarjetas horizontales

**Diapositiva 15: Cierre**
- Título: "¡Gracias!"
- Subtítulo: "¿Preguntas?"
- Información: "Proyecto de Analítica en Power BI | Bases de Datos 2026-1"
- Diseño: Fondo azul oscuro con círculos decorativos, texto centrado grande

---

### Instrucciones Adicionales para Gamma

1. **Usa el modo "Professional" o "Business"** para un tono académico pero moderno
2. **Incorpora iconos de Flaticon o similar** para cada sección (trofeos, balones, gráficos, etc.)
3. **Agrega transiciones suaves** entre diapositivas
4. **Usa animaciones de entrada** para elementos clave (números KPI, barras de gráficos)
5. **Mantén consistencia visual**: mismos colores, mismas fuentes, mismos estilos de tarjetas en toda la presentación
6. **Optimiza para proyección**: texto grande, contraste alto, poco texto por slide
7. **Incluye notas del presentador** con el contenido detallado que debe decirse en cada slide

### Contenido para Notas del Presentador

**Slide 1 (30 seg):** "Buenos días. Hoy presentamos nuestro proyecto de analítica de datos aplicado a los Mundiales de Fútbol."

**Slide 2 (1 min):** "La Copa Mundial es el evento deportivo más visto del planeta. Con 22 ediciones, 964 partidos y 2,720 goles, representa un caso ideal para aprender analítica de datos."

**Slide 3 (1 min):** "Nuestro objetivo fue diseñar un dashboard interactivo que permitiera explorar esta historia de forma navegable y útil."

**Slide 4 (1 min):** "Utilizamos el repositorio World Cup Database de Joshua Fjelstul, validado contra FIFA.com y otras fuentes oficiales."

**Slide 5 (2 min):** "El proceso ETL se realizó en Python con Pandas: extrajimos 18 CSV, los limpiamos y transformamos, y los cargamos en un esquema estrella."

**Slide 6 (2 min):** "El modelo tiene 5 dimensiones (torneo, equipo, jugador, fecha, fase) y 3 tablas de hechos (partidos, goles, desempeño por torneo)."

**Slide 7-9 (4 min):** "Demostración del dashboard: página ejecutiva con KPIs, página de campeones con análisis comparativo, y página de goleadores con ranking histórico."

**Slide 10-11 (3 min):** "Hallazgos clave: Brasil domina con 5 títulos, Suiza 1954 fue el torneo más ofensivo, y el 66.5% de los goles se anotan en fase de grupos."

**Slide 12 (1 min):** "Validamos todos los datos contra fuentes oficiales: FIFA, StatBunker, Transfermarkt y RSSSF."

**Slide 13 (1 min):** "Identificamos limitaciones como datos incompletos de jugadores, y proponemos mejoras como análisis predictivo."

**Slide 14 (30 seg):** "Entregamos 5 productos: el reporte Power BI, dataset limpio, diccionario de datos, documento de validación y metodología."

**Slide 15 (30 seg):** "Gracias por su atención. ¿Tienen preguntas?"

---

### Palabras Clave para Gamma

Usa estos términos para guiar el estilo:
- Moderno
- Minimalista
- Profesional
- Deportivo
- Analítico
- Visual
- Limpio
- Elegante
- Académico pero accesible

### Referencias Visuales (opcional)

Si Gamma permite subir referencias:
- Presentaciones de TED Talks (estilo limpio)
- Dashboards de Tableau Public (estilo de visualización)
- Infografías deportivas de ESPN o FIFA.com
