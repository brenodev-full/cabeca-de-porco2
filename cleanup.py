import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Remove Instagram button from loc-actions
html = re.sub(r'<a class="btn btn-ghost" href="https://instagram\.com"[^>]*>Instagram</a>', '', html)

# Remove Instagram and Facebook social links from footer socials
html = re.sub(r'<a aria-label="Instagram" href="https://instagram\.com"[^>]*>◎</a>', '', html)
html = re.sub(r'<a aria-label="Facebook" href="https://facebook\.com"[^>]*>f</a>', '', html)

# Remove the .reveal forced style since we'll handle it in JS now
html = html.replace('<style>.reveal { opacity: 1 !important; transform: none !important; }</style>', '')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Done')
