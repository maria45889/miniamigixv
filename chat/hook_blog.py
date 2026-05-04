import sys
sys.stdout.reconfigure(encoding='utf-8')

content = open('chat/templates/chat/index.html', encoding='utf-8').read()

old = "if (view === 'eventos') setTimeout(renderCalendar, 100);\n        }"
new = "if (view === 'eventos') setTimeout(renderCalendar, 100);\n            if (view === 'blog') cargarBlogs();\n        }"

# try both CR+LF and LF
replaced = content.replace(old, new, 1)
if replaced == content:
    old2 = "if (view === 'eventos') setTimeout(renderCalendar, 100);\r\n        }"
    new2 = "if (view === 'eventos') setTimeout(renderCalendar, 100);\r\n            if (view === 'blog') cargarBlogs();\r\n        }"
    replaced = content.replace(old2, new2, 1)

if replaced == content:
    print("COULD NOT FIND PATTERN - dumping context")
    idx = content.find("renderCalendar, 100)")
    print(repr(content[idx-5:idx+100]))
else:
    open('chat/templates/chat/index.html', 'w', encoding='utf-8').write(replaced)
    print('DONE')
