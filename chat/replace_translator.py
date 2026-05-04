import sys, re

content = open('chat/templates/chat/index.html', encoding='utf-8').read()

new_section = """        <!-- TRADUCTOR -->
        <section id="view-traductor" class="view-section">
            <div class="section-header">
                <h1 class="page-title">&#127760; Traductor Universal</h1>
            </div>

            <div style="display: flex; align-items: flex-end; gap: 12px; margin-bottom: 20px; flex-wrap: wrap;">
                <div style="flex: 1; min-width: 160px;">
                    <label style="font-size: 0.75rem; color: var(--txt-sub); display: block; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.06em;">Idioma de origen</label>
                    <select id="trans-from" style="width: 100%; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.12); border-radius: 12px; padding: 11px 14px; color: white; outline: none; font-size: 0.9rem;">
                        <option value="es">Espanol</option>
                        <option value="en">Ingles</option>
                        <option value="fr">Frances</option>
                        <option value="de">Aleman</option>
                        <option value="it">Italiano</option>
                        <option value="pt">Portugues</option>
                        <option value="ja">Japones</option>
                        <option value="ko">Coreano</option>
                        <option value="zh">Chino</option>
                        <option value="ru">Ruso</option>
                        <option value="ar">Arabe</option>
                        <option value="hi">Hindi</option>
                        <option value="tr">Turco</option>
                    </select>
                </div>
                <button onclick="swapLanguages()" style="flex-shrink: 0; background: rgba(126,232,250,0.1); border: 1px solid rgba(126,232,250,0.2); color: var(--acc-blue); border-radius: 50%; width: 44px; height: 44px; font-size: 1.3rem; cursor: pointer; transition: 0.2s;" onmouseover="this.style.background='rgba(126,232,250,0.25)'" onmouseout="this.style.background='rgba(126,232,250,0.1)'">&#8644;</button>
                <div style="flex: 1; min-width: 160px;">
                    <label style="font-size: 0.75rem; color: var(--txt-sub); display: block; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.06em;">Idioma de destino</label>
                    <select id="trans-to" style="width: 100%; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.12); border-radius: 12px; padding: 11px 14px; color: white; outline: none; font-size: 0.9rem;">
                        <option value="en">Ingles</option>
                        <option value="es">Espanol</option>
                        <option value="fr">Frances</option>
                        <option value="de">Aleman</option>
                        <option value="it">Italiano</option>
                        <option value="pt">Portugues</option>
                        <option value="ja">Japones</option>
                        <option value="ko">Coreano</option>
                        <option value="zh">Chino</option>
                        <option value="ru">Ruso</option>
                        <option value="ar">Arabe</option>
                        <option value="hi">Hindi</option>
                        <option value="tr">Turco</option>
                    </select>
                </div>
                <button onclick="translateText()" id="trans-btn" style="flex-shrink: 0; background: linear-gradient(135deg, var(--acc-blue), #4fa8c5); color: #000; border: none; border-radius: 12px; padding: 11px 28px; font-weight: 700; font-size: 0.9rem; cursor: pointer; height: 44px; transition: 0.2s;" onmouseover="this.style.opacity='0.85'" onmouseout="this.style.opacity='1'">TRADUCIR</button>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                <div style="display: flex; flex-direction: column; gap: 6px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-size: 0.75rem; color: var(--txt-sub); text-transform: uppercase; letter-spacing: 0.06em;">Texto original</span>
                        <button onclick="document.getElementById('trans-input').value=''; updateCharCount()" style="background: none; border: none; color: var(--txt-sub); font-size: 0.78rem; cursor: pointer; padding: 2px 6px;">Borrar</button>
                    </div>
                    <textarea id="trans-input" placeholder="Escribe o pega el texto aqui..." oninput="updateCharCount()" style="width: 100%; height: 220px; background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.1); border-radius: 14px; padding: 16px; color: white; outline: none; font-size: 0.92rem; resize: none; font-family: inherit; line-height: 1.6; box-sizing: border-box; transition: 0.2s;" onfocus="this.style.borderColor='rgba(126,232,250,0.35)'" onblur="this.style.borderColor='rgba(255,255,255,0.1)'"></textarea>
                    <span id="char-count" style="font-size: 0.75rem; color: var(--txt-sub); text-align: right;">0 / 500</span>
                </div>
                <div style="display: flex; flex-direction: column; gap: 6px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-size: 0.75rem; color: var(--txt-sub); text-transform: uppercase; letter-spacing: 0.06em;">Traduccion</span>
                        <button onclick="copyTranslation()" style="background: none; border: none; color: var(--acc-blue); font-size: 0.78rem; cursor: pointer; padding: 2px 6px;">Copiar</button>
                    </div>
                    <div id="trans-output" style="width: 100%; height: 220px; background: rgba(126,232,250,0.03); border: 1px solid rgba(126,232,250,0.12); border-radius: 14px; padding: 16px; color: rgba(255,255,255,0.85); font-size: 0.92rem; line-height: 1.6; overflow-y: auto; box-sizing: border-box;">
                        <span style="color: rgba(255,255,255,0.25); font-style: italic;">La traduccion aparecera aqui...</span>
                    </div>
                    <span style="font-size: 0.72rem; color: rgba(255,255,255,0.2); text-align: right;">Powered by MyMemory</span>
                </div>
            </div>

            <div style="margin-top: 20px;">
                <p style="font-size: 0.75rem; color: var(--txt-sub); text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 10px;">Frases rapidas</p>
                <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                    <button onclick="quickPhrase('Como estas?')" style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); color: var(--txt-main); border-radius: 20px; padding: 6px 14px; font-size: 0.8rem; cursor: pointer; transition: 0.2s;" onmouseover="this.style.background='rgba(255,255,255,0.12)'" onmouseout="this.style.background='rgba(255,255,255,0.05)'">Como estas?</button>
                    <button onclick="quickPhrase('Hola, mucho gusto')" style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); color: var(--txt-main); border-radius: 20px; padding: 6px 14px; font-size: 0.8rem; cursor: pointer; transition: 0.2s;" onmouseover="this.style.background='rgba(255,255,255,0.12)'" onmouseout="this.style.background='rgba(255,255,255,0.05)'">Hola, mucho gusto</button>
                    <button onclick="quickPhrase('Muchas gracias')" style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); color: var(--txt-main); border-radius: 20px; padding: 6px 14px; font-size: 0.8rem; cursor: pointer; transition: 0.2s;" onmouseover="this.style.background='rgba(255,255,255,0.12)'" onmouseout="this.style.background='rgba(255,255,255,0.05)'">Muchas gracias</button>
                    <button onclick="quickPhrase('Te quiero mucho')" style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); color: var(--txt-main); border-radius: 20px; padding: 6px 14px; font-size: 0.8rem; cursor: pointer; transition: 0.2s;" onmouseover="this.style.background='rgba(255,255,255,0.12)'" onmouseout="this.style.background='rgba(255,255,255,0.05)'">Te quiero mucho</button>
                    <button onclick="quickPhrase('Tengo hambre')" style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); color: var(--txt-main); border-radius: 20px; padding: 6px 14px; font-size: 0.8rem; cursor: pointer; transition: 0.2s;" onmouseover="this.style.background='rgba(255,255,255,0.12)'" onmouseout="this.style.background='rgba(255,255,255,0.05)'">Tengo hambre</button>
                    <button onclick="quickPhrase('No hablo este idioma')" style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); color: var(--txt-main); border-radius: 20px; padding: 6px 14px; font-size: 0.8rem; cursor: pointer; transition: 0.2s;" onmouseover="this.style.background='rgba(255,255,255,0.12)'" onmouseout="this.style.background='rgba(255,255,255,0.05)'">No hablo este idioma</button>
                </div>
            </div>
        </section>"""

old_start = content.find('<section id="view-traductor"')
old_end = content.find('</section>', old_start) + len('</section>')

# Find leading whitespace before old_start
pre = content[:old_start]
comment_start = pre.rfind('\n')
new_content = content[:comment_start+1] + new_section + '\n' + content[old_end:]

open('chat/templates/chat/index.html', 'w', encoding='utf-8').write(new_content)
print('DONE')
