#!/usr/bin/env python3
with open("build_dashboard.py", "r", encoding="utf-8") as f:
    text = f.read()

# Replace initClickSpark with guarded version
old_init = "(function initClickSpark() {\n      const canvas = document.createElement('canvas');"
new_init = "(function initClickSpark() {\n      if (typeof window === 'undefined' || typeof document === 'undefined' || !document.body) return;\n      const canvas = document.createElement('canvas');"
text = text.replace(old_init, new_init)

# Guard document.addEventListener
old_mouse = "document.addEventListener('mousemove', (e) => {"
new_mouse = "if (typeof document !== 'undefined' && document.addEventListener) document.addEventListener('mousemove', (e) => {"
text = text.replace(old_mouse, new_mouse)

with open("build_dashboard.py", "w", encoding="utf-8") as f:
    f.write(text)

print("Safeguards patched.")
