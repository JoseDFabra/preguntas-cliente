# Matriz de casos y de riesgo

El objetivo es que ningún «¿qué pasa si…?» quede sin dueño. Cada caso termina en
uno de tres lugares: ya lo resuelve el código, lo decide el desarrollador, o lo
decide el cliente.

## 1. Mapa del flujo

Antes de buscar casos, sale del código (no de los specs, que pueden estar
desactualizados) la lista de:

- **Pasos y estados**: enums de estado, columnas `estado`, funciones que cambian
  de estado. Qué estados existen y qué transiciones permite el código.
- **Actores**: roles, permisos, quién ejecuta cada paso, quién no tiene cuenta.
- **Reglas duras**: validaciones que lanzan error (`throw`, `BadRequest`,
  `Conflict`), restricciones únicas, chequeos en el servicio.
- **Tiempos**: vencimientos, plazos, fechas por defecto, tareas programadas.
- **Avisos**: correos, notificaciones, a quién y cuándo.
- **Documentos**: formatos oficiales, plantillas, qué se imprime y qué no.
- **Valores por defecto**: lo que el sistema propone y el usuario puede cambiar.

Anota para cada regla dónde vive (`archivo:línea`). Es lo que permite decir «así
está hoy» con certeza.

## 2. Situaciones a cruzar con cada paso

Recorre cada paso del flujo con esta lista. No todas aplican a todos los pasos;
la lista existe para no olvidar ninguna.

| Situación | Preguntas guía |
|---|---|
| Camino feliz | ¿Está claro quién hace qué y en qué orden? ¿El orden es obligatorio? |
| Ausencia | ¿Y si no responde, no asiste, no tiene el dato, no tiene correo o contacto? |
| Tiempo | ¿Y si vence, llega tarde, se adelanta, se salta un período? ¿Cuánto es el plazo? ¿Días hábiles o corridos? |
| Error y corrección | ¿Y si se equivocó? ¿Se puede corregir después de cerrado, firmado o enviado? ¿Queda rastro? |
| Quién | ¿Quién puede hacerlo, verlo, autorizarlo? ¿Y si lo hace otra persona en su nombre? |
| Excepción | ¿Casos especiales: anónimos, varios a la vez, montos o fechas fuera de lo normal? |
| Repetición | ¿Puede pasar más de una vez? (varios pagos, varias visitas, varios aprobadores) |
| Avisos | ¿A quién se le avisa, por qué medio, y en qué momentos? |
| Formato | ¿Hay un formato oficial? ¿Qué campos lleva? ¿Se genera, se adjunta o se firma? |
| Fin | ¿Cuándo termina? ¿Quién lo cierra? ¿Se puede reabrir? |

## 3. Clasificar cada caso

| Clase | Significa | Qué se hace |
|---|---|---|
| **Resuelto** | El código ya lo maneja y es razonable | No se pregunta; puede ir a la tabla de «lo que ya funciona» o a los supuestos |
| **Técnico** | La respuesta depende de cómo está hecho el sistema | Va a la entrevista con el desarrollador, nunca al cliente |
| **Negocio** | La respuesta es una regla de la institución | Va al cliente, con la opción actual marcada |
| **Ya decidido** | Está en `docs/decisiones-cliente.md` o en un spec aprobado | No se vuelve a preguntar, salvo que el código lo contradiga |

## 4. Prioridad por riesgo

Califica cada caso de negocio del 1 al 3 en dos ejes:

- **Probabilidad**: 1 rara vez, 2 algunas veces al mes, 3 pasa casi siempre.
- **Impacto si se decide mal**: 1 molestia, 2 retrabajo o dato incorrecto,
  3 documento oficial errado, problema legal, dato sensible expuesto o pérdida
  de información.

| Puntaje (prob × impacto) | Destino |
|---|---|
| 6 a 9 | Pregunta con opciones, en las primeras secciones |
| 3 a 4 | Pregunta corta |
| 1 a 2 | Supuesto que se aprueba en bloque |

Un impacto 3 nunca va a supuestos, aunque sea raro: si sale mal, sale muy mal.

Tope por ronda: unas 25 a 30 preguntas. Si sobran, quedan las de menor puntaje
para la siguiente ronda y se dice en el resumen al desarrollador.

## 5. Guarda la matriz

Escribe la matriz completa en `revision-pendientes/matriz-<tema>.md` como tabla:
paso, situación, clase, cómo está hoy (`archivo:línea`), puntaje, destino. La
página para el cliente es solo una vista de esa matriz; la matriz es lo que
permite saber en la siguiente ronda qué se cubrió.
