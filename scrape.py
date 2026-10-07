import os
import re
import urllib.request
from urllib.parse import urljoin

base_url = "https://id-preview--3ad22999-3e01-4088-9ae8-b548569548b2.lovable.app"
html_file = "index_utf8.html"
output_file = "cabeça de porco.html"

with open(html_file, 'r', encoding='utf-8') as f:
    html = f.read()

# Find all /assets/ links
asset_pattern = re.compile(r'(/assets/[^"\'\s>]+)')
assets = asset_pattern.findall(html)
assets = list(set(assets)) # unique

os.makedirs('assets', exist_ok=True)

# Download assets
for asset in assets:
    url = urljoin(base_url, asset)
    local_path = "." + asset # ./assets/...
    print(f"Downloading {url} to {local_path}")
    try:
        urllib.request.urlretrieve(url, local_path)
    except Exception as e:
        print(f"Failed to download {url}: {e}")

# Remove lovable traces
html = re.sub(r'<meta name="author" content="Lovable"/>', '', html)
html = re.sub(r'<meta name="twitter:site" content="@Lovable"/>', '', html)
# Remove the lovable badge style and html
html = re.sub(r'<style>.*?#lovable-badge.*?</style>', '', html, flags=re.DOTALL)
html = re.sub(r'<aside\s+id="lovable-badge".*?</aside>', '', html, flags=re.DOTALL)
html = re.sub(r'<script>.*?lovable-badge.*?</script>', '', html, flags=re.DOTALL)
html = re.sub(r'<script src="https://cdn\.gpteng\.co/lovable\.js" type="module"></script>', '', html)

# Modify asset paths to relative (already relative in HTML but let's make sure)
html = html.replace('href="/assets/', 'href="assets/')
html = html.replace('src="/assets/', 'src="assets/')
html = html.replace('url(/assets/', 'url(assets/')

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html)

print("Done")
