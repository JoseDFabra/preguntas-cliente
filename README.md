# preguntas-cliente

Skill para Claude Code que convierte el flujo de un sistema en preguntas de reglas de negocio para el cliente. Entrevista primero al desarrollador para resolver lo técnico, genera una página `dudas-<tema>.html` que el cliente llena y devuelve como mensaje, y lleva el registro de decisiones en `docs/decisiones-cliente.md`.

## Instalación

```bash
git clone https://github.com/JoseDFabra/preguntas-cliente ~/.claude/skills/preguntas-cliente
```

Requiere Python 3. Queda disponible en la siguiente sesión de Claude Code. Para actualizar: `git pull` dentro de esa carpeta.

## Uso

`/preguntas-cliente`, `/preguntas-cliente <tema>`, o pídele a Claude que revise un flujo con el cliente. Para procesar respuestas, pega el mensaje que devolvió el cliente.

La primera vez en cada proyecto pregunta el nombre de quien recibe las respuestas, el cliente y el color, y los guarda en `revision-pendientes/datos.json` del proyecto.
