import re
from bs4 import BeautifulSoup

def update_html():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')

    # 1. Remove search box
    search_box = soup.find('div', class_='search-box')
    if search_box:
        search_box.decompose()

    # 2. Remove 24/7 from About stats
    for stat in soup.find_all('div', class_='stat'):
        num = stat.find('div', class_='num')
        if num and '24/7' in num.text:
            stat.decompose()

    # 3. Remove Horário from loc-row
    for loc_row in soup.find_all('div', class_='loc-row'):
        lbl = loc_row.find('div', class_='lbl')
        if lbl and 'Horário' in lbl.text:
            loc_row.decompose()

    # 4. Remove Aberto 24h from footer
    for li in soup.find_all('li'):
        if 'Aberto 24h' in li.text:
            li.decompose()

    # 5. Build new menu-grid
    menu_grid = soup.find('div', class_='menu-grid')
    if menu_grid:
        menu_grid.clear()

        menu_data = [
            # Entradas
            {"cat": "entradas", "name": "Peppa Pig", "price": "R$ 35,90", "desc": "5 unidades de bolinha de Pulled Pork com cream cheese recheado de mozzarella, na cama de cheddar."},
            {"cat": "entradas", "name": "Croquete de Costela Bovina", "price": "R$ 32,90", "desc": "5 unidades de croquete de costela bovina defumada. Acompanha molho de pimenta agridoce."},
            {"cat": "entradas", "name": "João Frango", "price": "R$ 35,90", "desc": "5 unidades da nossa versão de coxinha sem massa, desta vez com frango defumado. Acompanha mostarda e mel."},
            {"cat": "entradas", "name": "Linguiça", "price": "R$ 34,90", "desc": "100% pernil suíno com queijo gratinado. Acompanha farofa de cuscuz e chimichurri fresco."},
            {"cat": "entradas", "name": "Escondidinho", "price": "R$ 27,90", "desc": "De pulled pork com creme de aipim cremoso e muito queijo."},
            {"cat": "entradas", "name": "Torresmo de Rolo", "price": "R$ 34,90", "desc": "De carne clara, macia e suculenta com a pururuca crocante."},
            {"cat": "entradas", "name": "Torresmo Pipoca", "price": "R$ 17,90", "desc": "Só o biscoitinho, pele suína bem crocante."},
            {"cat": "entradas", "name": "Porção de Pastel - Pulled Pork", "price": "R$ 38,90", "desc": "Com 6 unidades. Pastel de carne suína desfiada e defumada por 12h."},
            {"cat": "entradas", "name": "Porção de Pastel - Pulled Pork c/ Cream Cheese", "price": "R$ 38,90", "desc": "Com 6 unidades. Pastel de carne suína desfiada e defumada por 12h com cream cheese."},
            {"cat": "entradas", "name": "Porção de Pastel - Queijo", "price": "R$ 38,90", "desc": "Com 6 unidades. Pastel de mozzarella argentina."},
            {"cat": "entradas", "name": "Batata Simples", "price": "R$ 25,90", "desc": "Ou aipim. Acompanha molho da casa."},
            {"cat": "entradas", "name": "Batata com Cheddar e Bacon", "price": "R$ 29,90", "desc": "Batata frita coberta com cheddar e bacon."},
            {"cat": "entradas", "name": "Batata com Cheddar e Pulled Pork", "price": "R$ 32,90", "desc": "Batata frita coberta com cheddar e pulled pork."},
            {"cat": "entradas", "name": "Batata com Sour Cream e Pastrami", "price": "R$ 36,90", "desc": "Batata frita com sour cream e pastrami."},

            # Hamburgueres
            {"cat": "hamburgueres", "name": "Chris Cornell", "price": "R$ 29,90", "desc": "Pão brioche, carne bovina 200g, mozzarella argentina, maionese da casa, cebola roxa, alface americana e sweet pickle."},
            {"cat": "hamburgueres", "name": "Slash", "price": "R$ 29,90", "desc": "Pão brioche, carne bovina 200g defumada, mozzarella, ketchup, mostarda amarela e relish de pepino com cebola."},
            {"cat": "hamburgueres", "name": "Led Zeppelin", "price": "R$ 31,90", "desc": "Pão brioche, carne bovina 200g, molho cheddar, geléia de pimenta e fatia de bacon."},
            {"cat": "hamburgueres", "name": "Freddie Mercury", "price": "R$ 31,90", "desc": "Pão brioche, sobrecoxa defumada, mozzarella, maionese de páprica, alface americana e cebola roxa."},
            {"cat": "hamburgueres", "name": "Choripan", "price": "R$ 28,00", "desc": "Feito no pão francês com aquele queimadinho argentino, recheado com 2 linguiças suínas, bastante mozzarella argentina e chimichurri fresco."},
            {"cat": "hamburgueres", "name": "Clássico", "price": "R$ 21,90", "desc": "Pão brioche, carne 100g com mozzarella e ketchup."},

            # Pitsmoker
            {"cat": "pitsmoker", "name": "Costela Suína (Inteira)", "price": "R$ 89,90", "desc": "Costela suína defumada em lenha frutífera no estilo American BBQ. Acompanha Sweet Pickle e Molho Barbecue."},
            {"cat": "pitsmoker", "name": "Costela Suína (Meia)", "price": "R$ 59,90", "desc": "Meia porção de costela suína defumada em lenha frutífera. Acompanha Sweet Pickle e Molho Barbecue."},
            {"cat": "pitsmoker", "name": "Costela Bovina", "price": "R$ 99,90", "desc": "Costela bovina defumada cortada em cubos finalizada com manteiga de garrafa e cebola. Acompanha batata ou aipim frito."},

            # Grelhados
            {"cat": "grelhados", "name": "Tábua de Ancho", "price": "R$ 99,90", "desc": "Steak de Ancho com 4 linguiças de cordeiro e 1 pão de alho. Acompanha salada de cebola, farofa de cuscuz e geléia de hortelã."},
            {"cat": "grelhados", "name": "Picanha Bovina", "price": "R$ 119,90", "desc": "Picanha Bovina grelhada com mozzarela gratinada. Acompanha farofa de cuscuz e vinagrete."},
            {"cat": "grelhados", "name": "Chorizo com Gorgonzola", "price": "R$ 69,90", "desc": "Steak de chorizo com queijo gorgonzola. Acompanha cebola caramelizada e farofa de cuscuz."},

            # Bebidas
            {"cat": "bebidas", "name": "Água sem gás", "price": "R$ 4,00", "desc": ""},
            {"cat": "bebidas", "name": "Água com gás", "price": "R$ 5,00", "desc": ""},
            {"cat": "bebidas", "name": "Água Tônica", "price": "R$ 6,00", "desc": ""},
            {"cat": "bebidas", "name": "Coca Cola", "price": "R$ 6,00", "desc": "Normal e zero"},
            {"cat": "bebidas", "name": "Guaraná Antártica", "price": "R$ 6,00", "desc": "Normal e zero"},
            {"cat": "bebidas", "name": "Sprite", "price": "R$ 6,00", "desc": ""},
            {"cat": "bebidas", "name": "Fanta Uva", "price": "R$ 6,00", "desc": ""},
            {"cat": "bebidas", "name": "Fanta Laranja", "price": "R$ 6,00", "desc": ""},
            {"cat": "bebidas", "name": "Mate", "price": "R$ 6,00", "desc": ""},
            {"cat": "bebidas", "name": "Del Vale Uva", "price": "R$ 6,00", "desc": ""},
            {"cat": "bebidas", "name": "Del Vale Pêssego", "price": "R$ 6,00", "desc": ""},
            {"cat": "bebidas", "name": "Limoneto", "price": "R$ 8,00", "desc": ""},
            {"cat": "bebidas", "name": "Heineken Zero", "price": "R$ 10,00", "desc": ""},

            # Alcoólicas
            {"cat": "alcoolicas", "name": "Jack Daniel's", "price": "R$ 18,00", "desc": "Lemonade / Cola"},
            {"cat": "alcoolicas", "name": "Stella", "price": "R$ 8,00", "desc": "LongNeck"},
            {"cat": "alcoolicas", "name": "Corona", "price": "R$ 9,00", "desc": "LongNeck"},
            {"cat": "alcoolicas", "name": "Heineken LongNeck", "price": "R$ 10,00", "desc": "LongNeck"},
            {"cat": "alcoolicas", "name": "Budweiser", "price": "R$ 9,00", "desc": "LongNeck"},
            {"cat": "alcoolicas", "name": "Pinkmoon", "price": "R$ 14,90", "desc": "600ml"},
            {"cat": "alcoolicas", "name": "Heineken 600ml", "price": "R$ 17,00", "desc": "600ml"},
            {"cat": "alcoolicas", "name": "Brahma Duplo Malte", "price": "R$ 12,00", "desc": "600ml"},
            {"cat": "alcoolicas", "name": "Spaten", "price": "R$ 14,00", "desc": "600ml"},
            {"cat": "alcoolicas", "name": "Colorado Lager Ribeirão", "price": "R$ 16,00", "desc": "600ml"},

            # Especiais
            {"cat": "especiais", "name": "Tacos Suínos (Quarta)", "price": "R$ 28,90", "desc": "3 unidades de tortilhas recheadas com carne suína ao molho thai com sour cream e picles jalapeño."},
            {"cat": "especiais", "name": "Festival de Espetos (Quarta)", "price": "R$ 0,00", "desc": "Feitos na parrilla. Acompanhem no dia."},
            {"cat": "especiais", "name": "Pastrami Mustard (Quinta)", "price": "R$ 42,90", "desc": "Produto 100% artesanal de fabricação própria servido com molho de mostarda da casa e salada de rúcula no pão de miga."},
            {"cat": "especiais", "name": "Cheese Pastrami (Quinta)", "price": "R$ 42,90", "desc": "Servido no pão de miga, acompanha queijo mozzarella e sweet pickle."},
            {"cat": "especiais", "name": "Sanduba Bovino (Quinta)", "price": "R$ 38,00", "desc": "Carne bovina grelhada com maionese de páprica, mozzarella argentina e sweet pickle."},
            {"cat": "especiais", "name": "Tacos Suínos (Quinta)", "price": "R$ 28,90", "desc": "3 unidades de tortilhas recheadas com carne suína ao molho thai com sour cream e picles jalapeño."},

            # Almoço de Domingo
            {"cat": "almoco-de-domingo", "name": "Costela Suína", "price": "R$ 129,90", "desc": "Rack de costela suína defumada em lenha frutífera besuntada em molho agridoce. Serve 2 pessoas."},
            {"cat": "almoco-de-domingo", "name": "Prime Rib Suíno", "price": "R$ 105,90", "desc": "2 unidades do Prime Rib suíno levemente defumado. Serve 2 pessoas."},
            {"cat": "almoco-de-domingo", "name": "Pork Belly Ribs", "price": "R$ 139,90", "desc": "Costela suína com pururuca crocante em cima. Serve 2 pessoas."},
            {"cat": "almoco-de-domingo", "name": "Picanha Bovina", "price": "R$ 149,90", "desc": "Picanha bovina grelhada."},
            {"cat": "almoco-de-domingo", "name": "Prime Rib Bovino Defumado", "price": "R$ 179,90", "desc": "Corte nobre retirado do lombo com prolongação da costela. Serve 2 pessoas."},
            {"cat": "almoco-de-domingo", "name": "Tábua de Ancho", "price": "R$ 139,90", "desc": "Steak de ancho bovino com 4 linguiças de cordeiro e 1 pão de alho. Serve 2 pessoas."},
            {"cat": "almoco-de-domingo", "name": "Tábua de Frango Defumado", "price": "R$ 99,90", "desc": "4 sobrecoxas de frango desossadas e defumadas, finalizada com molho da casa."},
            {"cat": "almoco-de-domingo", "name": "Costela Bovina em Cubos", "price": "R$ 149,90", "desc": "Costela bovina defumada cortada em cubos, finalizada com manteiga de garrafa e cebola. Serve 2 pessoas."},
            {"cat": "almoco-de-domingo", "name": "Arroz Branco (Acompanhamento Extra)", "price": "R$ 15,00", "desc": ""},
            {"cat": "almoco-de-domingo", "name": "BBQ Beans (Acompanhamento Extra)", "price": "R$ 29,90", "desc": "Feijão defumado"},
            {"cat": "almoco-de-domingo", "name": "Farofa de cuscuz (Acompanhamento Extra)", "price": "R$ 8,00", "desc": ""},
            {"cat": "almoco-de-domingo", "name": "Molho vinagrete (Acompanhamento Extra)", "price": "R$ 8,00", "desc": ""},
        ]

        for item in menu_data:
            article = soup.new_tag('article', **{'class': 'menu-item', 'data-category': item['cat']})
            
            # For testing layout visibility, start with only entradas visible
            if item['cat'] != 'entradas':
                article['style'] = 'display: none; opacity: 0; transform: translateY(10px);'
            else:
                article['style'] = 'opacity: 1; transform: translateY(0); transition: opacity 0.4s ease, transform 0.4s ease;'

            head = soup.new_tag('div', **{'class': 'menu-item-head'})
            h4 = soup.new_tag('h4')
            h4.string = item['name']
            dots = soup.new_tag('span', **{'class': 'menu-dots'})
            price = soup.new_tag('span', **{'class': 'menu-price'})
            price.string = item['price']
            
            head.append(h4)
            head.append(dots)
            head.append(price)
            article.append(head)

            if item['desc']:
                p = soup.new_tag('p')
                p.string = item['desc']
                article.append(p)
            
            foot = soup.new_tag('div', **{'class': 'menu-foot'})
            foot_span = soup.new_tag('span')
            btn = soup.new_tag('button', **{'class': 'add-btn'})
            if item['price'] == "R$ 0,00":
                btn.string = "Consultar"
            else:
                btn.string = "+ Adicionar"
            
            foot.append(foot_span)
            foot.append(btn)
            article.append(foot)

            menu_grid.append(article)

    # 6. Update tabs data-target
    tabs_container = soup.find('div', class_='tabs')
    if tabs_container:
        tab_mapping = {
            'Entradas': 'entradas',
            'Hambúrgueres': 'hamburgueres',
            'Pitsmoker': 'pitsmoker',
            'Grelhados': 'grelhados',
            'Bebidas': 'bebidas',
            'Alcoólicas': 'alcoolicas',
            'Especiais': 'especiais',
            'Almoço de Domingo': 'almoco-de-domingo'
        }
        for tab in tabs_container.find_all('button', class_='tab'):
            target = tab_mapping.get(tab.text.strip())
            if target:
                tab['data-target'] = target

    with open('index.html', 'w', encoding='utf-8') as f:
        # Prevent bs4 from writing out a fully expanded html that breaks format
        # Actually bs4 might reformat it slightly but it's fine.
        f.write(str(soup))

if __name__ == '__main__':
    update_html()
