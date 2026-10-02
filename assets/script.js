  (function () {
    const form = document.getElementById('revision');
    const KEY = '__CLAVE__';
    const $ = id => document.getElementById(id);
    const val = id => ($(id)?.value || '').trim();
    const campos = () => form.querySelectorAll('input, textarea');
    const preguntas = () => [...form.querySelectorAll('.pregunta[data-question]')];
    const TOTAL = preguntas().length;

    function guardar() {
      const data = {};
      campos().forEach(el => {
        if (el.id === 'mensaje') return;
        if (el.type === 'radio') { if (el.checked) data[el.name] = el.value; }
        else if (el.type === 'checkbox') data[el.id] = el.checked;
        else data[el.id] = el.value;
      });
      const aviso = $('guardado');
      try {
        localStorage.setItem(KEY, JSON.stringify(data));
        const hora = new Date().toLocaleTimeString('es-CO', { hour: 'numeric', minute: '2-digit' });
        aviso.textContent = 'Guardado automáticamente · ' + hora;
        aviso.className = 'guardado ok';
      } catch (e) {
        aviso.textContent = 'Este navegador no está guardando lo que escribe. Termine y genere el mensaje sin cerrar la página.';
        aviso.className = 'guardado error';
      }
      aviso.hidden = false;
    }
    function cargar() {
      let data = null;
      try { data = JSON.parse(localStorage.getItem(KEY) || 'null'); } catch (e) {}
      if (!data) return;
      const llenos = Object.values(data).filter(v => v === true || (typeof v === 'string' && v.trim() !== '')).length;
      if (!llenos) return;
      $('guardado').textContent = 'Se recuperó lo que había llenado antes.';
      $('guardado').className = 'guardado ok';
      $('guardado').hidden = false;
      campos().forEach(el => {
        if (el.type === 'radio') el.checked = data[el.name] === el.value;
        else if (el.type === 'checkbox') el.checked = data[el.id] === true;
        else if (el.id in data) el.value = data[el.id];
      });
    }

    function respuesta(el) {
      const q = el.dataset.question;
      const marcadas = [...el.querySelectorAll('input:checked')].map(i => i.value);
      return { opciones: marcadas, detalle: val(q + '-det') };
    }
    const respondida = el => { const r = respuesta(el); return r.opciones.length > 0 || r.detalle !== ''; };

    // «Con cambios» o «No apruebo» sin decir qué cambiar no le sirve a nadie.
    function sinObservacion() {
      return [...form.querySelectorAll('.aprobar[data-item]')].filter(el => {
        const r = form.querySelector('input[name="' + el.dataset.item + '"]:checked');
        return r && r.value !== 'Aprobado' && !val(el.dataset.item + '-obs');
      });
    }

    function progreso() {
      const n = preguntas().filter(respondida).length;
      $('progreso').textContent = 'Ha respondido ' + n + ' de ' + TOTAL + ' preguntas.' +
        (n < TOTAL ? ' Las que deje en blanco quedarán como pendientes.' : '');
      form.querySelectorAll('.aprobar textarea.falta').forEach(t => {
        if (!sinObservacion().some(el => el.contains(t))) t.classList.remove('falta');
      });
    }

    function mensaje() {
      const general = form.querySelector('input[name="general"]:checked');
      const fecha = new Date().toLocaleDateString('es-CO', { day: 'numeric', month: 'long', year: 'numeric' });
      const L = [];
      L.push('Hola __DESTINATARIO__, respondí __ASUNTO__.');
      L.push('');
      L.push('¿SEGUIR CONSTRUYENDO CON ESTAS RESPUESTAS?: ' + general.value.toUpperCase());
      if (val('general-obs')) L.push(val('general-obs'));
      L.push('');
      L.push('CÓMO QUEDÓ LO CONSTRUIDO');
      [...form.querySelectorAll('.aprobar[data-item]')].filter(el => el.dataset.item !== 'general').forEach(el => {
        const id = el.dataset.item;
        const r = form.querySelector('input[name="' + id + '"]:checked');
        L.push('- ' + el.dataset.label + ': ' + (r ? r.value : 'Sin revisar'));
        if (val(id + '-obs')) L.push('  Cambios: ' + val(id + '-obs'));
      });

      const pendientes = [];
      L.push('');
      L.push('RESPUESTAS');
      preguntas().forEach((el, i) => {
        const r = respuesta(el);
        if (!r.opciones.length && !r.detalle) { pendientes.push(i + 1); return; }
        L.push('');
        L.push((i + 1) + '. ' + el.dataset.label);
        if (r.opciones.length) L.push('   Respuesta: ' + r.opciones.join('; '));
        if (r.detalle) L.push('   Detalle: ' + r.detalle);
      });
      if (pendientes.length) { L.push(''); L.push('Sin responder: ' + pendientes.join(', ')); }


      if (val('otros')) { L.push(''); L.push('OTRAS OBSERVACIONES'); L.push(val('otros')); }
      L.push('');
      L.push(val('nombre') + (val('cargo') ? ' — ' + val('cargo') : ''));
      L.push(fecha);
      return L.join('\n');
    }

    cargar();
    progreso();
    form.addEventListener('input', () => { guardar(); progreso(); });
    form.addEventListener('change', () => { guardar(); progreso(); });
    // Por si el navegador cierra la pestaña antes de que termine un tecleo.
    window.addEventListener('pagehide', guardar);
    document.addEventListener('visibilitychange', () => { if (document.visibilityState === 'hidden') guardar(); });
    form.addEventListener('submit', e => {
      e.preventDefault();
      const aviso = $('aviso');
      const faltan = [];
      const obs = sinObservacion();
      form.querySelectorAll('.falta').forEach(t => t.classList.remove('falta'));
      obs.forEach(el => $(el.dataset.item + '-obs').classList.add('falta'));
      if (obs.length) faltan.push('escriba qué cambiaría en: ' + obs.map(el => el.dataset.label.toLowerCase()).join('; '));
      if (!form.querySelector('input[name="general"]:checked')) faltan.push('marque si podemos seguir construyendo con estas respuestas');
      if (!val('nombre')) faltan.push('escriba su nombre');
      if (faltan.length) {
        aviso.textContent = 'Antes de generar el mensaje, ' + faltan.join('; y ') + '.';
        aviso.hidden = false;
        if (obs.length) $(obs[0].dataset.item + '-obs').focus();
        return;
      }
      aviso.hidden = true;
      $('mensaje').value = mensaje();
      $('estado').textContent = '';
      $('resultado').hidden = false;
      $('resultado').scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
    $('copiar').addEventListener('click', () => {
      const t = $('mensaje');
      const ok = () => { $('estado').textContent = 'Copiado. Ahora péguelo en el mensaje para __DESTINATARIO__.'; };
      const manual = () => { t.focus(); t.select(); $('estado').textContent = 'Presione Ctrl+C (o Cmd+C en Mac) para copiar.'; };
      try { navigator.clipboard.writeText(t.value).then(ok, () => { t.select(); try { document.execCommand('copy') ? ok() : manual(); } catch (e) { manual(); } }); }
      catch (e) { manual(); }
    });
    $('volver').addEventListener('click', () => { window.scrollTo({ top: 0, behavior: 'smooth' }); });
  })();
