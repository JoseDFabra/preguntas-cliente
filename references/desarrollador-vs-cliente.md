# Qué se le pregunta al desarrollador y qué al cliente

El cliente sabe cómo funciona su proceso; no sabe, ni tiene por qué saber, cómo
está hecho el sistema. Una pregunta técnica le quita confianza en el sistema y
en la página entera, y además la responde mal. Por eso todo lo técnico se
resuelve antes con el desarrollador.

## La prueba

> ¿Una persona del área, que nunca ha visto el código, puede responder esto
> sabiendo solo cómo trabaja su dependencia?

- Sí → es del cliente.
- No, o la respuesta depende de una limitación técnica → es del desarrollador.
- Las dos cosas → se parte: el desarrollador dice qué es posible y el cliente
  escoge entre las opciones posibles.

## Va al desarrollador

- **Infraestructura**: servidor, SMTP y cuentas de correo, dominios, Docker,
  respaldos, variables de entorno, integraciones con otros sistemas.
- **Diferencias entre el spec y el código**: el diseño dice una cosa y el
  código hace otra. ¿Cuál es la verdad? ¿Es un bug o un cambio de decisión?
- **Bugs o huecos encontrados al leer el código**: permisos mal puestos,
  validaciones que faltan. No son preguntas para el cliente; se reportan.
- **Factibilidad y costo**: antes de ofrecerle al cliente una opción, ¿se puede
  construir? ¿Cuánto cuesta? Una opción que no se va a construir no se ofrece.
- **Lo que el desarrollador ya sabe del cliente**: conversaciones que no quedaron
  escritas. Si ya lo dijo, no se le vuelve a preguntar.
- **Datos de la ronda**: nombre del cliente o del área, a quién se le envía el
  mensaje de respuesta, color del proyecto, si es primera ronda o seguimiento.
- **Confirmar las lecturas dudosas de «así está hoy»** cuando el código admite
  dos interpretaciones.
- **Qué preguntas sobran**: el desarrollador puede tachar las que considera ya
  resueltas o fuera de alcance.

## Va al cliente

Reglas de la institución: quién hace qué, en qué orden, plazos, qué pasa en cada
excepción, a quién se avisa, qué formatos existen, qué se imprime, quién
aprueba, qué es obligatorio.

## Cómo hacer la entrevista

- Usa `AskUserQuestion` en rondas de hasta 4 preguntas, con opciones concretas y
  la recomendada primero. Las preguntas al desarrollador sí pueden ser técnicas.
- Empieza por los datos de la ronda, luego bugs y diferencias spec/código, luego
  factibilidad de las opciones que piensas ofrecer, y al final la lista de
  preguntas de negocio para que tache o agregue.
- Para mostrarle la lista de preguntas de negocio, escríbela en texto agrupada por
  sección, con su puntaje, y pregunta cuáles quitar, cuáles agregar y si alguna
  ya la respondió el cliente.
- Lo que el desarrollador decida queda en `docs/decisiones-cliente.md` con la
  marca «decidido por desarrollo», para que no vuelva a aparecer.
- No hagas más de tres rondas. Si quedan dudas técnicas sin responder, sácalas
  de la página del cliente y déjalas como pendientes del desarrollador.

## Traducción al idioma del cliente

Al pasar una pregunta al cliente, quita la jerga:

| No escribir | Escribir |
|---|---|
| token, link con hash | enlace |
| endpoint, API, ruta | (no se menciona) |
| estado `BORRADOR`, enum | borrador, en espera, aprobado |
| rol, permiso `EDICION` | quién puede ver, quién puede cambiar |
| migración, base de datos, columna | (no se menciona) |
| validación, se lanza error | el sistema no deja / el sistema avisa |
| campo nulo, vacío por defecto | queda en blanco |
| usuario sin cuenta | persona que no entra al sistema |
| SMTP, servidor de correo | el correo institucional |

Si la pregunta no se puede escribir sin esas palabras, probablemente es del
desarrollador.
