import re

def process_html():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Remove CP
    html = html.replace('<div class="brand-mark">CP</div>', '')

    # 2. Add Organization Comments
    html = html.replace('<header class="nav">', '<!-- ==========================================\n     CABEÇALHO (HEADER) E MENU DE NAVEGAÇÃO\n     ========================================== -->\n    <header class="nav">')
    html = html.replace('<section class="hero" id="home">', '<!-- ==========================================\n     SEÇÃO 1: HERO (BANNERS E CHAMADA PRINCIPAL)\n     ========================================== -->\n    <section class="hero" id="home">')
    html = html.replace('<section class="features" id="diferenciais">', '<!-- ==========================================\n     SEÇÃO 2: DIFERENCIAIS (ÍCONES E VANTAGENS)\n     ========================================== -->\n    <section class="features" id="diferenciais">')
    html = html.replace('<section id="cardapio">', '<!-- ==========================================\n     SEÇÃO 3: CARDÁPIO DIGITAL\n     ========================================== -->\n    <section id="cardapio">')
    html = html.replace('<section class="about" id="sobre">', '<!-- ==========================================\n     SEÇÃO 4: SOBRE NÓS (HISTÓRIA)\n     ========================================== -->\n    <section class="about" id="sobre">')
    
    html = re.sub(r'(<section[^>]*id="localizacao"[^>]*>)', r'<!-- ==========================================\n     SEÇÃO 5: LOCALIZAÇÃO E MAPA\n     ========================================== -->\n    \1', html)
    html = re.sub(r'(<section[^>]*id="contato"[^>]*>)', r'<!-- ==========================================\n     SEÇÃO 6: CONTATO E RODAPÉ\n     ========================================== -->\n    \1', html)
    html = html.replace('<footer', '<!-- ==========================================\n     RODAPÉ (FOOTER)\n     ========================================== -->\n    <footer')

    # 3. Add responsive CSS
    css_to_add = """
        /* === RESPONSIVIDADE (CELULAR) === */
        @media (max-width: 768px) {
            .nav {
                flex-direction: column;
                padding: 15px;
            }
            .nav-links {
                display: none; /* Em telas pequenas, o menu fica oculto ou precisaria de script para abrir */
            }
            .hero-content h1 {
                font-size: 2.5rem;
            }
            .feature-grid, .menu-grid, .about-grid {
                display: grid;
                grid-template-columns: 1fr;
                gap: 20px;
            }
            .tabs {
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                gap: 10px;
            }
            .hero-bg {
                background-position: center;
            }
            .about-stats {
                flex-direction: column;
            }
        }
    """
    html = html.replace('</style>', f'{css_to_add}\n    </style>')

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print('Done!')

if __name__ == '__main__':
    process_html()
