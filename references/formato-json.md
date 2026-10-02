# Formato de dudas-<tema>.json

```json
{
  "titulo": "Preguntas pendientes del préstamo de equipos",
  "titulo_corto": "Dudas préstamos",
  "lead": "El sistema ya registra las solicitudes de préstamo. Aquí está cómo quedó cada cosa y las preguntas que faltan.",
  "destinatario": "<quien recibe las respuestas>",
  "asunto": "las preguntas pendientes del préstamo de equipos",
  "clave": "dudas-prestamos-v1",
  "color": "#2F4A6D",
  "color_suave": "#EBEFF5",
  "pregunta_otros": "¿Hay algo del préstamo de equipos que no se preguntó?",
  "secciones": [
    {
      "titulo": "Lo que ya funciona en el sistema",
      "parrafos": ["Cada fila es algo que el sistema ya hace hoy."],
      "tabla": [
        { "que": "Solicitar un equipo", "como": "La persona elige el equipo y las fechas.", "estado": "Hecho" }
      ],
      "aprobar": "¿Funciona como usted lo esperaba?",
      "id": "construido"
    },
    {
      "titulo": "La aprobación del préstamo",
      "parrafos": ["Antes se aprobaba por correo. Ahora queda en el sistema:"],
      "flujo": ["La persona solicita", { "texto": "El jefe aprueba", "nota": "paso nuevo", "nuevo": true }, "Se entrega el equipo"],
      "lista": ["Si el jefe no responde en <strong>3 días</strong>, la solicitud vence."],
      "aprobar": "¿Aprueba que el préstamo se apruebe así?",
      "preguntas": [
        {
          "id": "plazo-aprobacion",
          "texto": "¿Cuántos días tiene el jefe para aprobar?",
          "ayuda": "Si es otro plazo, escríbalo abajo.",
          "opciones": [
            { "texto": "3 días", "marca": "hoy" },
            "5 días hábiles",
            { "texto": "No vence: espera hasta que responda", "marca": "prop" }
          ]
        },
        {
          "id": "enviar",
          "texto": "¿Qué nos puede enviar?",
          "varias": true,
          "opciones": ["El formato de préstamo", "El inventario de equipos"]
        }
      ]
    }
  ],
  "supuestos": [
    "Una persona no puede tener dos préstamos del mismo equipo al mismo tiempo."
  ]
}
```

## Campos

| Campo | Obligatorio | Uso |
|---|---|---|
| `titulo`, `titulo_corto` | sí | Encabezado de la página y título de la pestaña |
| `lead` | sí | Párrafo de entrada. Admite `<strong>` |
| `destinatario` | sí | A quién le envía el cliente el mensaje |
| `asunto` | sí | Completa «Hola X, respondí …» en el mensaje |
| `clave` | sí | Llave del guardado en el navegador. **Única por ronda**: si dos páginas comparten clave, las respuestas de una aparecen en la otra |
| `color`, `color_suave` | no | Acento del proyecto. Por defecto un azul neutro |
| `minutos` | no | Si se omite se calcula por el número de preguntas |
| `pregunta_otros` | no | La pregunta abierta del final |
| `secciones[]` | sí | En orden. Cada una puede traer `parrafos`, `tabla`, `flujo`, `lista`, `aprobar` y `preguntas` |
| `secciones[].id` | no | Id de la aprobación; por defecto `seccion-N` |
| `preguntas[].id` | sí | Único en toda la página, en minúsculas con guiones |
| `preguntas[].varias` | no | `true` para casillas de selección múltiple |
| `opciones[]` | sí | Texto plano, u objeto con `marca`: `"hoy"` o `"prop"` |
| `supuestos[]` | no | Reglas de bajo riesgo que se aprueban en bloque, en una sección propia antes del cierre |

La sección «Para terminar» (pregunta abierta, aprobación general, nombre, cargo y
botón del mensaje) la agrega el generador; no va en el JSON.

Los textos de `parrafos`, `lista`, `lead` y `ayuda` se insertan como HTML. Los de
preguntas, opciones, títulos y tabla se escapan.
