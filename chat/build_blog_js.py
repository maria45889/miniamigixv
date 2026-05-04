import sys
sys.stdout.reconfigure(encoding='utf-8')

content = open('chat/templates/chat/index.html', encoding='utf-8').read()

blog_js = '''
        // ════════════════════════════════════════
        //  BLOG
        // ════════════════════════════════════════
        let blogData = [];

        async function cargarBlogs() {
            try {
                const res = await fetch('/blog/listar/');
                const data = await res.json();
                blogData = data.blogs;
                renderBlogs();
            } catch(e) {
                document.getElementById('blog-list').innerHTML = '<p style="color:#f87171; text-align:center; padding:30px;">Error al cargar entradas.</p>';
            }
        }

        function renderBlogs() {
            const list = document.getElementById('blog-list');
            const counter = document.getElementById('blog-count');
            if (!list) return;

            counter.textContent = blogData.length + ' entradas';

            if (blogData.length === 0) {
                list.innerHTML = '<div style="text-align:center; padding:50px 20px; color:var(--txt-sub);"><div style="font-size:3rem; margin-bottom:12px;">&#9998;</div><p>Todavia no tienes entradas. Escribe tu primera!</p></div>';
                return;
            }

            list.innerHTML = blogData.map(b => {
                const preview = b.contenido.length > 150 ? b.contenido.substring(0, 150) + '...' : b.contenido;
                return \`<div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; padding: 20px; transition: 0.2s; cursor: default;" onmouseover="this.style.borderColor='rgba(167,139,250,0.25)'" onmouseout="this.style.borderColor='rgba(255,255,255,0.08)'">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px; gap: 10px;">
                        <h3 style="font-size: 1rem; color: var(--txt-main); font-weight: 700; margin: 0; line-height: 1.3;">\${escapeHtml(b.titulo)}</h3>
                        <div style="display: flex; gap: 6px; flex-shrink: 0;">
                            <button onclick="editarBlog(\${b.id})" style="background: rgba(167,139,250,0.1); border: 1px solid rgba(167,139,250,0.2); color: var(--acc-purple); border-radius: 8px; padding: 5px 10px; font-size: 0.75rem; cursor: pointer; transition: 0.2s;" onmouseover="this.style.background='rgba(167,139,250,0.2)'" onmouseout="this.style.background='rgba(167,139,250,0.1)'">Editar</button>
                            <button onclick="eliminarBlog(\${b.id})" style="background: rgba(248,113,113,0.08); border: 1px solid rgba(248,113,113,0.15); color: #f87171; border-radius: 8px; padding: 5px 10px; font-size: 0.75rem; cursor: pointer; transition: 0.2s;" onmouseover="this.style.background='rgba(248,113,113,0.18)'" onmouseout="this.style.background='rgba(248,113,113,0.08)'">Borrar</button>
                        </div>
                    </div>
                    <p style="font-size: 0.83rem; color: var(--txt-sub); line-height: 1.5; margin: 0 0 10px;">\${escapeHtml(preview)}</p>
                    <div style="font-size: 0.72rem; color: rgba(255,255,255,0.25);">\${b.creado_en}</div>
                </div>\`;
            }).join('');
        }

        async function guardarBlog() {
            const titulo = document.getElementById('blog-titulo').value.trim();
            const contenido = document.getElementById('blog-contenido').value.trim();
            const editId = document.getElementById('blog-edit-id').value;

            if (!titulo || !contenido) {
                showToast('Escribe un titulo y contenido', '&#9998;');
                return;
            }

            const url = editId ? \`/blog/editar/\${editId}/\` : '/blog/crear/';

            try {
                const res = await fetch(url, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json', 'X-CSRFToken': getCsrfToken()},
                    body: JSON.stringify({titulo, contenido, publicado: true})
                });
                const data = await res.json();
                if (data.status === 'ok') {
                    showToast(editId ? 'Entrada actualizada' : 'Entrada guardada', '&#10003;');
                    cancelarEditarBlog();
                    cargarBlogs();
                }
            } catch(e) {
                showToast('Error al guardar', '&#10007;');
            }
        }

        function editarBlog(id) {
            const b = blogData.find(x => x.id === id);
            if (!b) return;
            document.getElementById('blog-titulo').value = b.titulo;
            document.getElementById('blog-contenido').value = b.contenido;
            document.getElementById('blog-edit-id').value = id;
            document.getElementById('blog-form-title').textContent = 'Editando entrada';
            document.getElementById('blog-cancel-btn').style.display = 'block';
            document.getElementById('blog-titulo').focus();
        }

        function cancelarEditarBlog() {
            document.getElementById('blog-titulo').value = '';
            document.getElementById('blog-contenido').value = '';
            document.getElementById('blog-edit-id').value = '';
            document.getElementById('blog-form-title').textContent = '+ Nueva entrada';
            document.getElementById('blog-cancel-btn').style.display = 'none';
        }

        async function eliminarBlog(id) {
            if (!confirm('Borrar esta entrada permanentemente?')) return;
            try {
                const res = await fetch(\`/blog/eliminar/\${id}/\`, {
                    method: 'POST',
                    headers: {'X-CSRFToken': getCsrfToken()}
                });
                const data = await res.json();
                if (data.status === 'ok') {
                    showToast('Entrada eliminada', '&#128465;');
                    cargarBlogs();
                }
            } catch(e) {
                showToast('Error al eliminar', '&#10007;');
            }
        }

        function getCsrfToken() {
            const cookie = document.cookie.split(';').find(c => c.trim().startsWith('csrftoken='));
            return cookie ? cookie.split('=')[1] : '';
        }

'''

# Insert before </script>
close_script = '    </script>'
idx = content.rfind(close_script)
new_content = content[:idx] + blog_js + '    </script>' + content[idx + len(close_script):]

open('chat/templates/chat/index.html', 'w', encoding='utf-8').write(new_content)
print('DONE - Blog JS added')
