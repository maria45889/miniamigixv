import sys
sys.stdout.reconfigure(encoding='utf-8')

content = open('chat/templates/chat/index.html', encoding='utf-8').read()

new_blog = '''        <!-- BLOG -->
        <section id="view-blog" class="view-section">
            <div class="section-header">
                <h1 class="page-title">&#9998; Mi Blog Personal</h1>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1.6fr; gap: 20px; align-items: start;">

                <!-- Panel izquierdo: Escribir nueva entrada -->
                <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 20px; padding: 24px; position: sticky; top: 20px;">
                    <h3 id="blog-form-title" style="font-size: 1rem; color: var(--acc-purple); margin-bottom: 16px; font-weight: 700;">+ Nueva entrada</h3>
                    <input type="hidden" id="blog-edit-id" value="">
                    <div style="display: flex; flex-direction: column; gap: 12px;">
                        <input type="text" id="blog-titulo" placeholder="Titulo de tu entrada..." maxlength="255" style="width: 100%; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 12px 16px; color: white; outline: none; font-size: 0.9rem; box-sizing: border-box;" onfocus="this.style.borderColor='rgba(167,139,250,0.4)'" onblur="this.style.borderColor='rgba(255,255,255,0.1)'">
                        <textarea id="blog-contenido" placeholder="Escribe aqui tu entrada... Puedes escribir sobre tu dia, tus pensamientos, ideas, lo que quieras!" style="width: 100%; height: 200px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 12px 16px; color: white; outline: none; font-size: 0.88rem; resize: vertical; font-family: inherit; line-height: 1.6; box-sizing: border-box;" onfocus="this.style.borderColor='rgba(167,139,250,0.4)'" onblur="this.style.borderColor='rgba(255,255,255,0.1)'"></textarea>
                        <div style="display: flex; gap: 8px;">
                            <button onclick="guardarBlog()" style="flex: 1; background: linear-gradient(135deg, #a78bfa, #7c3aed); color: #fff; border: none; border-radius: 12px; padding: 11px; font-weight: 700; font-size: 0.88rem; cursor: pointer; transition: 0.2s;" onmouseover="this.style.opacity='0.85'" onmouseout="this.style.opacity='1'">GUARDAR</button>
                            <button onclick="cancelarEditarBlog()" id="blog-cancel-btn" style="display:none; flex: 0 0 auto; background: rgba(255,255,255,0.06); color: var(--txt-sub); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 11px 16px; font-size: 0.88rem; cursor: pointer;">Cancelar</button>
                        </div>
                    </div>
                </div>

                <!-- Panel derecho: Lista de entradas -->
                <div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                        <span style="font-size: 0.75rem; color: var(--txt-sub); text-transform: uppercase; letter-spacing: 0.06em;">Mis entradas</span>
                        <span id="blog-count" style="font-size: 0.75rem; background: rgba(167,139,250,0.12); color: var(--acc-purple); padding: 3px 10px; border-radius: 10px; font-weight: 700;">0 entradas</span>
                    </div>
                    <div id="blog-list" style="display: flex; flex-direction: column; gap: 14px;">
                        <p style="color: var(--txt-sub); font-size: 0.85rem; text-align: center; padding: 40px 0;">Cargando entradas...</p>
                    </div>
                </div>
            </div>
        </section>'''

old_start = content.find('<section id="view-blog"')
old_end = content.find('</section>', old_start) + len('</section>')
pre = content[:old_start]
comment_start = pre.rfind('\n')
new_content = content[:comment_start+1] + new_blog + '\n' + content[old_end:]

open('chat/templates/chat/index.html', 'w', encoding='utf-8').write(new_content)
print('DONE - Blog section built')
