#!/usr/bin/env python3
with open("build_dashboard.py", "r", encoding="utf-8") as f:
    text = f.read()

# Safe getAttribute in runDecryptedText
text = text.replace(
    "const originalText = el.getAttribute('data-decrypted');",
    "if (!el || typeof el.getAttribute !== 'function') return;\n        const originalText = el.getAttribute('data-decrypted');"
)

# Safe getAttribute in runCountUp
text = text.replace(
    "const targetStr = el.getAttribute('data-countup');",
    "if (!el || typeof el.getAttribute !== 'function') return;\n        const targetStr = el.getAttribute('data-countup');"
)

# Safe card.style.setProperty
text = text.replace(
    "card.style.setProperty('--mouse-x', `${x}px`);",
    "if (card.style && card.style.setProperty) card.style.setProperty('--mouse-x', `${x}px`);"
)
text = text.replace(
    "card.style.setProperty('--mouse-y', `${y}px`);",
    "if (card.style && card.style.setProperty) card.style.setProperty('--mouse-y', `${y}px`);"
)
text = text.replace(
    "card.style.setProperty('--cursor-angle', `${angle}deg`);",
    "if (card.style && card.style.setProperty) card.style.setProperty('--cursor-angle', `${angle}deg`);"
)

with open("build_dashboard.py", "w", encoding="utf-8") as f:
    f.write(text)

print("getAttribute safeguards applied.")
