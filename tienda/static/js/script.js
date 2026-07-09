document.addEventListener('DOMContentLoaded', function () {
    const modal = document.getElementById('productoModal');
    const cerrarModalBtn = document.getElementById('cerrarModalBtn');
    const seguirComprandoBtn = document.getElementById('seguirComprandoBtn');
    const agregarCarritoBtn = document.getElementById('agregarCarritoBtn');
    const cantidadProducto = document.getElementById('cantidadProducto');
    const modalProductoNombre = document.getElementById('modalProductoNombre');
    const modalProductoPrecio = document.getElementById('modalProductoPrecio');
    const modalProductoImagen = document.getElementById('modalProductoImagen');
    const modalImgPlaceholder = document.getElementById('modalImgPlaceholder');
    const modalProductoEspecificaciones = document.getElementById('modalProductoEspecificaciones');
    const modalProductoRecomendado = document.getElementById('modalProductoRecomendado');
    const modalFeedback = document.getElementById('modalFeedback');
    const carritoBadge = document.getElementById('carritoBadge');
    let productoSeleccionadoId = null;

    if (!modal) return;

    // ── Helpers ────────────────────────────────────────────────
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            document.cookie.split(';').forEach(function (c) {
                const cookie = c.trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                }
            });
        }
        return cookieValue;
    }

    function actualizarBadgeCarrito(totalItems) {
        if (!carritoBadge) return;
        const total = parseInt(totalItems, 10) || 0;
        carritoBadge.textContent = total;
        total > 0 ? carritoBadge.classList.remove('d-none') : carritoBadge.classList.add('d-none');
    }

    function formatCLP(n) {
        return '$' + Math.abs(parseInt(n || 0)).toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.');
    }

    // ── Formatear descripción ──────────────────────────────────
    function renderDescripcion(descripcion, specsLabel) {
        if (!modalProductoEspecificaciones || !modalProductoRecomendado) return;
        modalProductoEspecificaciones.innerHTML = '';
        modalProductoRecomendado.innerHTML = '';
        modalProductoRecomendado.style.display = 'none';

        if (!descripcion || descripcion.trim() === '') return;

        const partes = descripcion.split('|').map(p => p.trim()).filter(Boolean);
        const specs = [];
        let recomendado = '';

        partes.forEach(function (p) {
            const lower = p.toLowerCase();
            if (lower.startsWith('recomendado') || lower.startsWith('promocion valida')) {
                recomendado = p;
            } else {
                specs.push(p);
            }
        });

        // Renderizar specs como badges/etiquetas
        if (specs.length > 0) {
            const titulo = document.createElement('p');
            titulo.className = 'mb-1 fw-semibold text-muted';
            titulo.style.fontSize = '0.78rem';
            titulo.style.textTransform = 'uppercase';
            titulo.style.letterSpacing = '0.5px';
            titulo.textContent = specsLabel || 'Especificaciones técnicas';
            modalProductoEspecificaciones.appendChild(titulo);

            const grid = document.createElement('div');
            grid.className = 'specs-grid';
            specs.forEach(function (spec) {
                const badge = document.createElement('span');
                badge.className = 'spec-badge';
                badge.textContent = spec;
                grid.appendChild(badge);
            });
            modalProductoEspecificaciones.appendChild(grid);
        }

        // Renderizar recomendado / promoción (solo si hay contenido)
        if (recomendado) {
            const icono = recomendado.toLowerCase().startsWith('promocion') ? '🏷️' : '✅';
            modalProductoRecomendado.innerHTML =
                '<span class="recomendado-label">' + icono + ' ' + recomendado + '</span>';
            modalProductoRecomendado.style.display = '';
        }
    }

    // ── Abrir / cerrar modal ───────────────────────────────────
    function abrirModal(card) {
        productoSeleccionadoId = card.dataset.id || null;

        modalProductoNombre.textContent = card.dataset.nombre || '';
        modalProductoPrecio.innerHTML =
            formatCLP(card.dataset.precio || 0) +
            ' <small style="font-size:0.75rem;font-weight:400;color:#6b7280;">+ IVA</small>';

        if (card.dataset.imagen) {
            modalProductoImagen.src = card.dataset.imagen;
            modalProductoImagen.style.display = 'block';
            if (modalImgPlaceholder) modalImgPlaceholder.style.display = 'none';
        } else {
            modalProductoImagen.style.display = 'none';
            modalProductoImagen.removeAttribute('src');
            if (modalImgPlaceholder) modalImgPlaceholder.style.display = 'flex';
        }

        const specsLabel = modal.dataset.specsLabel || '';
        renderDescripcion(card.dataset.descripcion || '', specsLabel);

        if (cantidadProducto) cantidadProducto.value = '1';
        if (modalFeedback) modalFeedback.textContent = '';

        modal.classList.add('show');
        modal.style.display = 'flex';
        modal.setAttribute('aria-hidden', 'false');
    }

    function cerrarModal() {
        modal.classList.remove('show');
        modal.style.display = 'none';
        modal.setAttribute('aria-hidden', 'true');
    }

    // ── Listeners en tarjetas (toda la tarjeta es clickeable) ──
    document.querySelectorAll('.producto-card').forEach(function (card) {
        card.addEventListener('click', function (e) {
            // Ignorar clicks en otros elementos interactivos dentro de la tarjeta
            if (e.target.tagName === 'A' || e.target.tagName === 'INPUT') return;
            abrirModal(card);
        });
    });

    // ── Cerrar modal ───────────────────────────────────────────
    if (cerrarModalBtn) cerrarModalBtn.addEventListener('click', cerrarModal);
    if (seguirComprandoBtn) seguirComprandoBtn.addEventListener('click', cerrarModal);

    modal.addEventListener('click', function (e) {
        if (e.target === modal) cerrarModal();
    });

    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && modal.getAttribute('aria-hidden') === 'false') cerrarModal();
    });

    // ── Agregar al carrito ─────────────────────────────────────
    if (agregarCarritoBtn) {
        agregarCarritoBtn.addEventListener('click', function () {
            const cantidad = parseInt(cantidadProducto ? cantidadProducto.value : 1, 10);

            if (isNaN(cantidad) || cantidad < 1) {
                modalFeedback.textContent = 'Ingresa una cantidad válida (mínimo 1).';
                modalFeedback.style.color = '#dc3545';
                return;
            }
            if (!productoSeleccionadoId) {
                modalFeedback.textContent = 'No se pudo identificar el producto.';
                modalFeedback.style.color = '#dc3545';
                return;
            }

            fetch('/carrito/agregar/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ producto_id: productoSeleccionadoId, cantidad: cantidad })
            })
                .then(function (response) {
                    return response.json().then(function (data) {
                        return { ok: response.ok, data: data };
                    });
                })
                .then(function (result) {
                    if (!result.ok || !result.data.ok) {
                        throw new Error(result.data.mensaje || 'No fue posible agregar al carrito.');
                    }
                    modalFeedback.textContent = result.data.mensaje + ' (' + cantidad + ' unidad(es))';
                    modalFeedback.style.color = '#198754';
                    actualizarBadgeCarrito(result.data.total_items_carrito);
                })
                .catch(function (error) {
                    modalFeedback.textContent = error.message || 'Error al agregar al carrito.';
                    modalFeedback.style.color = '#dc3545';
                });
        });
    }
});

// ══════════════════════════════════════
//  CHAT REXI FLOTANTE
// ══════════════════════════════════════
(function () {
    const fab      = document.getElementById('wa-fab');
    const card     = document.getElementById('wa-card');
    const closeBtn = document.getElementById('wa-close');
    const messages = document.getElementById('wa-messages');
    const input    = document.getElementById('wa-input');
    const sendBtn  = document.getElementById('wa-send');
    const typing   = document.getElementById('wa-typing');
    const badge    = document.getElementById('wa-badge');
    if (!fab || !card || !messages || !input) return;

    const SK       = 'rexi_chat_closed';
    const CHAT_URL = '/chat/';

    // ── Helpers ──────────────────────────────────────
    function getCsrf() {
        const m = document.cookie.match(/csrftoken=([^;]+)/);
        return m ? m[1] : '';
    }

    function now() {
        return new Date().toLocaleTimeString('es-CL', { hour: '2-digit', minute: '2-digit' });
    }

    function escapeHtml(text) {
        return text.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
    }

    function formatMessage(text) {
        // 1. Extraer links de carrito antes de procesar
        // Link múltiple: /agregar_multiples/?items=...
        text = text.replace(
            /(?:🛒\s*\*?Agregar al carrito:\*?\s*)?(https?:\/\/[^\s]+\/agregar_multiples\/\?items=([^\s<"]+))/gi,
            function(match, url, items) { return '\x00CARRITO_MULTI:' + items + '\x00'; }
        );
        // Link individual: /agregar_rapido/ID/
        text = text.replace(
            /(?:🛒\s*\*?Agregar al carrito:\*?\s*)?(https?:\/\/[^\s]+\/agregar_rapido\/(\d+)\/[^\s]*)/gi,
            function(match, url, id) { return '\x00CARRITO:' + id + '\x00'; }
        );

        // 2. Convertir tablas markdown en <table> HTML
        text = text.replace(/^([ \t]*\|.+\|[ \t]*\n)([ \t]*\|[-| :]+\|[ \t]*\n)((?:[ \t]*\|.+\|[ \t]*\n?)*)/gm,
            function(block) {
                const lines = block.trim().split('\n').filter(function(l) { return l.trim(); });
                if (lines.length < 2) return block;

                function parseCells(line) {
                    return line.replace(/^\||\|$/g, '').split('|').map(function(c) { return c.trim(); });
                }

                function cellHtml(c) {
                    // Procesa bold/italic dentro de la celda
                    let s = escapeHtml(c);
                    s = s.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
                    s = s.replace(/\*(.+?)\*/g, '<em>$1</em>');
                    return s;
                }

                const headers = parseCells(lines[0]);
                const rows = lines.slice(2);

                let html = '<div class="wa-table-wrap"><table class="wa-table"><thead><tr>';
                headers.forEach(function(h) { html += '<th>' + cellHtml(h) + '</th>'; });
                html += '</tr></thead><tbody>';
                rows.forEach(function(row) {
                    const cells = parseCells(row);
                    const isTotals = cells.some(function(c) {
                        return /total|iva|despacho/i.test(c);
                    });
                    html += '<tr' + (isTotals ? ' class="wa-table-total"' : '') + '>';
                    cells.forEach(function(c) { html += '<td>' + cellHtml(c) + '</td>'; });
                    html += '</tr>';
                });
                html += '</tbody></table></div>';
                return '\x00TABLE\x00' + html + '\x00ENDTABLE\x00';
            }
        );

        // 3. Escapar el resto del texto
        let parts = text.split(/(\x00TABLE\x00[\s\S]*?\x00ENDTABLE\x00|\x00CARRITO:\d+\x00)/g);
        let s = parts.map(function(part) {
            if (part.startsWith('\x00TABLE\x00')) {
                return part.replace('\x00TABLE\x00', '').replace('\x00ENDTABLE\x00', '');
            }
            if (part.startsWith('\x00CARRITO:')) {
                return part; // se procesa abajo
            }
            let p = escapeHtml(part);
            p = p.replace(/\n/g, '<br>');
            p = p.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
            p = p.replace(/\*(.+?)\*/g, '<em>$1</em>');
            p = p.replace(/(https?:\/\/[^\s<"]+)/g,
                '<a href="$1" target="_blank" rel="noopener" style="color:inherit;text-decoration:underline;">$1</a>');
            return p;
        }).join('');

        // 4. Placeholders de carrito → botón
        s = s.replace(/\x00CARRITO_MULTI:([^\x00]+)\x00/g, function(m, items) {
            return '<a href="/agregar_multiples/?items=' + items + '" class="wa-cart-btn">'
                 + '<i class="bi bi-cart-plus-fill"></i> Agregar todo al carrito</a>';
        });
        s = s.replace(/\x00CARRITO:(\d+)\x00/g, function(m, id) {
            return '<a href="/agregar_rapido/' + id + '/" class="wa-cart-btn">'
                 + '<i class="bi bi-cart-plus-fill"></i> Agregar al carrito</a>';
        });

        return s;
    }

    function addMessage(text, role) {
        const div = document.createElement('div');
        div.className = 'wa-msg wa-msg--' + role;
        div.innerHTML = `
            <div class="wa-msg-bubble">${formatMessage(text)}</div>
            <div class="wa-msg-time">${now()}</div>`;
        messages.appendChild(div);
        messages.scrollTop = messages.scrollHeight;
    }

    function setTyping(on) {
        typing.style.display = on ? 'block' : 'none';
        if (on) messages.scrollTop = messages.scrollHeight;
    }

    // ── Abrir / cerrar ──────────────────────────────
    function openWidget() {
        card.classList.add('open');
        fab.classList.remove('pulse');
        if (badge) badge.style.opacity = '0';
        sessionStorage.removeItem(SK);
        input.focus();
    }

    function closeWidget() {
        card.classList.remove('open');
        sessionStorage.setItem(SK, '1');
    }

    fab.addEventListener('click', function () {
        card.classList.contains('open') ? closeWidget() : openWidget();
    });

    closeBtn.addEventListener('click', function (e) {
        e.stopPropagation();
        closeWidget();
    });

    // ── Enviar mensaje ──────────────────────────────
    function sendMessage() {
        const text = input.value.trim();
        if (!text || sendBtn.disabled) return;

        addMessage(text, 'user');
        input.value = '';
        sendBtn.disabled = true;
        setTyping(true);

        fetch(CHAT_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrf(),
            },
            body: JSON.stringify({ mensaje: text }),
        })
        .then(function(r) { return r.json(); })
        .then(function(data) {
            setTyping(false);
            addMessage(data.respuesta || 'Sin respuesta.', 'bot');
        })
        .catch(function() {
            setTyping(false);
            addMessage('⚠️ Error de conexión. Intenta de nuevo.', 'bot');
        })
        .finally(function() {
            sendBtn.disabled = false;
            input.focus();
        });
    }

    sendBtn.addEventListener('click', sendMessage);
    input.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); }
    });

    // ── Auto-popup a los 15 segundos ────────────────
    if (!sessionStorage.getItem(SK)) {
        setTimeout(function () {
            if (!card.classList.contains('open')) openWidget();
        }, 15000);
    }
})();
