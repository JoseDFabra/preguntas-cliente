---
name: preguntas-cliente
description: Prepara las preguntas de reglas de negocio que el cliente debe definir sobre un flujo del sistema (qué pasa si…, quién hace qué, plazos, excepciones, avisos, formatos) y las entrega en una página dudas-<tema>.html que el cliente llena y devuelve como mensaje. Antes de generar la página entrevista al desarrollador para resolver lo técnico, de modo que al cliente solo le lleguen reglas de negocio. También procesa las respuestas del cliente y lleva el registro de decisiones. Úsala cuando el usuario pida revisar un flujo con el cliente, armar dudas o preguntas pendientes, una matriz de casos o de riesgo, «qué pasa si…», validar reglas de negocio, o pegue la respuesta de un cliente a una página de preguntas, aunque no diga el nombre de la skill.
---

# Preguntas al cliente

Convierte el flujo de un sistema en preguntas que el cliente puede responder sin
saber nada de cómo está hecho, y deja constancia de lo que decide.

El principio que guía todo: **el cliente decide reglas de negocio; el
desarrollador resuelve lo técnico.** Una página llena de preguntas de
infraestructura le hace perder confianza al cliente y las responde mal. Por eso
siempre hay una entrevista con el desarrollador antes de generar la página.

## Modos

Lee el argumento con que se invocó:

| Argumento | Modo |
|---|---|
| vacío | Revisión completa del flujo del proyecto actual |
| un tema (`aprobaciones`, `pagos`) | Revisión de ese flujo o módulo |
| una pregunta (`¿qué pasa si el aprobador no responde?`) | Pregunta suelta |
| `respuestas`, o el usuario pega el mensaje del cliente | Procesar respuestas |

## Revisión completa o por tema

### 1. Contexto previo

- Busca `docs/decisiones-cliente.md` y lo que haya en `revision-pendientes/`
  (rondas anteriores, matrices). Lo ya decidido no se vuelve a preguntar.
- Lee los specs y planes del proyecto para saber qué está aprobado y qué está
  diseñado sin construir.
- **Las reglas se leen del código, no de los specs.** Los specs se desactualizan;
  si el código y el spec no coinciden, es una pregunta para el desarrollador.
  Para un proyecto grande, usa un agente Explore que devuelva el mapa del flujo
  con `archivo:línea` de cada regla.

### 2. Matriz de casos

Lee `references/matriz-casos.md` y arma la matriz: cada paso del flujo cruzado
con las situaciones (ausencia, tiempo, error, quién, excepción, repetición,
avisos, formato, fin). Clasifica cada caso como resuelto, técnico, de negocio o
ya decidido, y califica los de negocio por probabilidad × impacto.

Guarda la matriz en `revision-pendientes/matriz-<tema>.md`.

### 3. Entrevista al desarrollador

Lee `references/desarrollador-vs-cliente.md`. Antes de escribir una sola línea
de la página:

1. **Datos de la ronda** (si no los sabes de rondas anteriores): el nombre del
   desarrollador o de quien recibe las respuestas (va en `destinatario`; nunca
   lo supongas), cómo se llama el área o el cliente, color del
   proyecto, si es primera ronda o seguimiento.
   Guárdalos en el proyecto, en `revision-pendientes/datos.json`, para no
   volver a preguntarlos. Nada de un proyecto se escribe dentro de la skill:
   ni nombres, ni colores, ni ejemplos; la skill sirve igual para cualquiera.
2. **Lo técnico**: bugs encontrados, diferencias spec/código, dudas de
   infraestructura, lecturas dudosas de «así está hoy».
3. **Factibilidad**: las opciones que piensas ofrecerle al cliente, ¿se pueden
   construir? Una opción que no se va a construir no se ofrece.
4. **La lista de negocio**: muéstrale en texto las preguntas agrupadas por
   sección, con su puntaje, y pregunta cuáles quitar, cuáles ya respondió el
   cliente y cuáles faltan.

Usa `AskUserQuestion` (hasta 4 preguntas por llamada, la opción recomendada
primero) y no pases de tres rondas. Lo que el desarrollador decida va a
`docs/decisiones-cliente.md` como «decidido por desarrollo».

### 4. Escribir las preguntas

Escribe `revision-pendientes/dudas-<tema>.json` con el formato de
`references/formato-json.md`. Reglas de redacción, porque el lector es una
persona del área y no un técnico:

- Trato de usted, frases cortas, sin jerga (la tabla de traducción está en
  `references/desarrollador-vs-cliente.md`).
- Cada sección cuenta primero cómo funciona hoy y después pregunta.
- Cada pregunta de opción única marca con `"hoy"` lo que hace el sistema hoy, o
  con `"prop"` lo diseñado sin construir. Así el cliente sabe qué pasa si no
  responde, y el sistema sigue funcionando mientras tanto.
- Las opciones son reglas concretas y excluyentes, no «depende». El detalle libre
  va en el campo «Otra respuesta», que la página siempre trae.
- Los casos de bajo riesgo van a `supuestos`, que se aprueban en bloque.
- Entre 15 y 30 preguntas. Más que eso no se responde bien en una sentada.

### 5. Generar y verificar

```bash
python3 ~/.claude/skills/preguntas-cliente/scripts/generar.py \
  revision-pendientes/dudas-<tema>.json revision-pendientes/dudas-<tema>.html
```

Después:

- Comprueba el script de la página: extrae el `<script>` y pásalo por `node --check`.
- Toma una captura con Chrome headless a 900 px y a 520 px de ancho y mírala.
  Por debajo de unos 500 px el headless recorta la página; no es un error del
  diseño.
- Ábrela con `open` para el desarrollador.

### 6. Resumen al desarrollador

Corto: cuántas preguntas y en qué secciones, qué quedó como supuesto, qué quedó
para otra ronda, y los bugs o pendientes técnicos encontrados, que no van al
cliente pero sí deben quedar a la vista. Ofrece publicarla como Artifact si
prefiere mandar un enlace en vez del archivo.

## Pregunta suelta

Para una sola duda no hace falta la página. Igual:

1. Busca en el código cómo funciona hoy y en `docs/decisiones-cliente.md` si ya se
   decidió.
2. Si es técnica, respóndela tú o pregúntasela al desarrollador; no va al cliente.
3. Si es de negocio, arma un texto corto listo para WhatsApp o correo: contexto
   en una frase, la pregunta y las opciones numeradas, con la de hoy marcada
   «(así funciona hoy)». Si son más de 3 preguntas relacionadas, sugiere la página.

## Procesar respuestas

Cuando el desarrollador pega el mensaje que generó la página:

1. Ubica la página y la matriz de esa ronda para saber qué significaba cada
   respuesta.
2. Agrega a `docs/decisiones-cliente.md` una entrada por respuesta:

   ```markdown
   ## <fecha> · Ronda <n> · <tema> · respondió <nombre, cargo>

   | # | Pregunta | Respuesta | Cambia el sistema |
   |---|---|---|---|
   | 3 | ¿Cuántos días tiene para responder? | 5 días hábiles | Sí: el plazo pasa a días hábiles (`<archivo>`) |
   ```

3. Para cada respuesta que cambia el sistema, di qué archivo o qué parte del plan
   se toca. Una respuesta igual a «así está hoy» no cambia nada, pero queda
   registrada como confirmada.
4. Lista lo que quedó sin responder o con respuesta ambigua: eso es la siguiente
   ronda. Las aprobaciones «con cambios» o «no apruebo» se tratan como prioridad.
5. No cambies código en este paso: muestra el resumen y pregunta si actualiza el
   spec o el plan.

## Archivos de la skill

- `scripts/generar.py`: arma la página desde el JSON.
- `assets/estilo.css`, `assets/script.js`: diseño y comportamiento de la página
  (guardado automático, progreso, mensaje para copiar).
- `references/matriz-casos.md`: situaciones a revisar y matriz de riesgo.
- `references/desarrollador-vs-cliente.md`: qué es técnico, cómo entrevistar al
  desarrollador y cómo traducir la jerga.
- `references/formato-json.md`: el formato del archivo de preguntas, con ejemplo.
