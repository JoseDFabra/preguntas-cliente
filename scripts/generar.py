#!/usr/bin/env python3
"""Arma la página dudas-<tema>.html a partir de un JSON de preguntas.

Uso: python3 generar.py dudas.json salida.html

El diseño y el script (guardado en localStorage, progreso, mensaje para copiar)
salen de assets/. Así todas las rondas de todos
los proyectos se ven y se comportan igual; solo cambia el contenido.

Los textos de párrafos, listas e intro admiten HTML simple (<strong>). Los
textos de preguntas y opciones se escapan, porque también viajan como valores.
"""
import html
import json
import sys
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / 'assets'
e = html.escape


def aprobar(item, etiqueta, pregunta):
    return f'''
    <div class="aprobar" data-item="{e(item)}" data-label="{e(etiqueta)}">
      <p class="aprobar-t">{e(pregunta)}</p>
      <fieldset class="choices" aria-label="{e(etiqueta)}">
        <label><input type="radio" name="{e(item)}" id="{e(item)}-si" value="Aprobado"> Sí, apruebo</label>
        <label><input type="radio" name="{e(item)}" id="{e(item)}-cambios" value="Aprobado con cambios"> Sí, con cambios</label>
        <label><input type="radio" name="{e(item)}" id="{e(item)}-no" value="No aprobado"> No apruebo</label>
      </fieldset>
      <textarea id="{e(item)}-obs" placeholder="Si marca «con cambios» o «no apruebo», escriba qué cambiaría." aria-label="Observaciones: {e(etiqueta)}"></textarea>
    </div>'''


class Pagina:
    def __init__(self, datos):
        self.d = datos
        self.n = 0
        self.ids = set()

    def _id(self, valor):
        if valor in self.ids:
            sys.exit(f'Id repetido: {valor}. Cada pregunta y cada aprobación necesita un id único.')
        self.ids.add(valor)
        return valor

    def pregunta(self, p):
        self.n += 1
        q = self._id(p['id'])
        varias = p.get('varias', False)
        tipo = 'checkbox' if varias else 'radio'
        marcas = {'hoy': ' <em class="hoy">así está hoy</em>',
                  'prop': ' <em class="hoy prop">propuesta</em>'}
        filas = []
        for i, op in enumerate(p['opciones']):
            if isinstance(op, str):
                op = {'texto': op}
            filas.append(
                f'          <label><input type="{tipo}" name="{e(q)}" id="{e(q)}-{i}" value="{e(op["texto"])}"> '
                f'<span>{e(op["texto"])}{marcas.get(op.get("marca"), "")}</span></label>')
        ayuda = f'\n        <p class="ayuda">{p["ayuda"]}</p>' if p.get('ayuda') else ''
        return f'''
      <div class="pregunta" data-question="{e(q)}" data-tipo="{'check' if varias else 'radio'}" data-label="{e(p['texto'])}">
        <p class="pregunta-t" id="{e(q)}-t"><span class="n">{self.n}.</span> {e(p['texto'])}</p>{ayuda}
        <fieldset class="opciones" aria-labelledby="{e(q)}-t">
{chr(10).join(filas)}
        </fieldset>
        <textarea id="{e(q)}-det" placeholder="Otra respuesta o detalle (opcional)" aria-label="Otra respuesta o detalle: pregunta {self.n}"></textarea>
      </div>'''

    def seccion(self, num, s):
        partes = [f'\n  <section>\n    <h2><span class="num">{num}</span>{e(s["titulo"])}</h2>']
        for p in s.get('parrafos', []):
            partes.append(f'    <p>{p}</p>')
        if s.get('tabla'):
            filas = '\n'.join(
                f'        <tr><td>{e(f["que"])}</td><td>{e(f["como"])}</td>'
                f'<td><span class="est">{e(f["estado"])}</span></td></tr>' for f in s['tabla'])
            partes.append(f'''    <div class="scroll"><table>
      <thead><tr><th>Qué</th><th>Cómo funciona</th><th>Estado</th></tr></thead>
      <tbody>
{filas}
      </tbody>
    </table></div>''')
        if s.get('flujo'):
            pasos = []
            for paso in s['flujo']:
                if isinstance(paso, str):
                    paso = {'texto': paso}
                nota = f' <span>{e(paso["nota"])}</span>' if paso.get('nota') else ''
                clase = ' class="nuevo"' if paso.get('nuevo') else ''
                pasos.append(f'      <li{clase}>{e(paso["texto"])}{nota}</li>')
            partes.append(f'    <ol class="flujo" aria-label="{e(s["titulo"])}">\n' + '\n'.join(pasos) + '\n    </ol>')
        if s.get('lista'):
            partes.append('    <ul class="lista">\n' + '\n'.join(f'      <li>{x}</li>' for x in s['lista']) + '\n    </ul>')
        if s.get('aprobar'):
            item = self._id(s.get('id') or f'seccion-{num}')
            partes.append(aprobar(item, s['titulo'], s['aprobar']))
        if s.get('preguntas'):
            partes.append('\n    <div class="preguntas">\n      <h3 class="sub">Preguntas</h3>'
                          + ''.join(self.pregunta(p) for p in s['preguntas']) + '\n    </div>')
        partes.append('  </section>')
        return '\n'.join(partes)

    def render(self):
        d = self.d
        dest = d['destinatario']
        secciones = [self.seccion(i + 1, s) for i, s in enumerate(d['secciones'])]

        # Los supuestos de bajo riesgo se aprueban en bloque, sin una pregunta cada uno.
        if d.get('supuestos'):
            secciones.append(self.seccion(len(secciones) + 1, {
                'titulo': 'Lo que vamos a asumir',
                'id': 'supuestos',
                'parrafos': ['Estas reglas parecen claras y el sistema las va a seguir así. Si alguna no es correcta, márquelo y escriba cuál.'],
                'lista': d['supuestos'],
                'aprobar': '¿Está de acuerdo con estos supuestos?',
            }))

        num_final = len(secciones) + 1
        self._id('general')
        final = f'''
  <section>
    <h2><span class="num">{num_final}</span>Para terminar</h2>
    <div class="pregunta">
      <label for="otros" class="pregunta-t">{e(d.get('pregunta_otros', '¿Hay algo que no se preguntó y que el sistema debería tener en cuenta?'))}</label>
      <textarea id="otros" placeholder="Opcional"></textarea>
    </div>{aprobar('general', 'Seguir construyendo con estas respuestas', '¿Podemos seguir construyendo con estas respuestas?')}
    <div class="firma">
      <label for="nombre">Su nombre<input type="text" id="nombre"></label>
      <label for="cargo">Cargo o dependencia<input type="text" id="cargo"></label>
    </div>
    <div class="final">
      <p class="progreso" id="progreso" role="status"></p>
      <button type="submit" id="generar">Generar mensaje para {e(dest)}</button>
      <p class="aviso" id="aviso" hidden></p>
    </div>
    <div class="resultado" id="resultado" hidden>
      <h3>Listo. Copie este mensaje y envíeselo a {e(dest)}</h3>
      <p>Péguelo en un correo o en WhatsApp. Si quiere ajustar algo, puede editarlo aquí mismo antes de copiarlo.</p>
      <textarea id="mensaje" aria-label="Mensaje para {e(dest)}"></textarea>
      <div class="acciones">
        <button type="button" id="copiar">Copiar mensaje</button>
        <button type="button" class="sec" id="volver">Volver a revisar</button>
        <span class="estado" id="estado" role="status"></span>
      </div>
    </div>
  </section>'''

        hay_prop = '"hoy prop"' in ''.join(secciones)
        marcas = 'La opción marcada con «así está hoy» es la que el sistema usa mientras llega su respuesta.'
        if hay_prop:
            marcas += ' La marcada con «propuesta» es como se diseñó algo que todavía no está construido.'
        minutos = d.get('minutos') or max(5, round(self.n * 0.6))

        css = (ASSETS / 'estilo.css').read_text(encoding='utf-8')
        css = css.replace('__ACENTO__', d.get('color', '#2F4A6D')).replace('__ACENTO_SUAVE__', d.get('color_suave', '#EBEFF5'))
        js = (ASSETS / 'script.js').read_text(encoding='utf-8')
        js = (js.replace('__CLAVE__', d['clave']).replace('__DESTINATARIO__', dest.replace("'", "\\'"))
                .replace('__ASUNTO__', d['asunto'].replace("'", "\\'")))

        pasos = ''.join(f'\n      <li>{x}</li>' for x in [
            'Revise cómo quedó cada punto y marque si lo aprueba.',
            'Responda las preguntas: escoja una opción, o escriba la suya en «Otra respuesta». Si no sabe una, déjela en blanco.',
            f'Genere el mensaje, cópielo y envíeselo a {e(dest)}.'])

        return f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(d['titulo_corto'])}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Serif:wght@600&display=swap">
<style>
{css}</style>
</head>
<body>
<div class="wrap">
  <header>
    <h1>{e(d['titulo'])}</h1>
    <p class="lead">{d['lead']}</p>
    <ol class="pasos">{pasos}
    </ol>
    <p class="intro">Son {self.n} preguntas y toma unos {minutos} minutos. {marcas}</p>
    <p class="intro"><strong>Sus respuestas se guardan solas.</strong> Si cierra la página o se le apaga el computador, al volver a abrirla en este mismo navegador encontrará todo como lo dejó.</p>
  </header>
  <p class="guardado" id="guardado" role="status" aria-live="polite" hidden></p>

  <form id="revision" autocomplete="off" novalidate>{''.join(secciones)}
{final}
  </form>
</div>

<script>
{js}</script>
</body>
</html>
'''


def main():
    if len(sys.argv) != 3:
        sys.exit('Uso: python3 generar.py dudas.json salida.html')
    datos = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
    faltan = [k for k in ('titulo', 'titulo_corto', 'lead', 'destinatario', 'clave', 'asunto', 'secciones') if k not in datos]
    if faltan:
        sys.exit('Faltan campos en el JSON: ' + ', '.join(faltan))
    pagina = Pagina(datos)
    Path(sys.argv[2]).write_text(pagina.render(), encoding='utf-8')
    print(f'{sys.argv[2]}: {pagina.n} preguntas')
    if pagina.n > 30:
        print('Aviso: más de 30 preguntas. Pase las de bajo riesgo a «supuestos» o déjelas para otra ronda.')


if __name__ == '__main__':
    main()
