from parsel import Selector
import requests
import time
from tech_news.database import create_news

import json

# Requisito 1
def fetch(url):
    """Seu código deve vir aqui"""
    time.sleep(1)
    try:
        response = requests.get(url, timeout=3)
    except requests.Timeout:
        return None
    if response.status_code == 200:
        return response.text
    return None


# Requisito 2
def scrape_noticia(html_content):
    """Seu código deve vir aqui"""
    selector = Selector(text=html_content)
    url = selector.css('link[rel="canonical"]::attr(href)').get()
    title = selector.css('h1.tec--article__header__title::text').get()
    timestamp = selector.css('time::attr(datetime)').get()

    get_writer = selector.css('a.tec--author__info__link::text').get()
    writer = get_writer.strip() if (get_writer) else None

    get_shares_count = selector.css('div.tec--toolbar__item::text').get()
    shares_count = int(
        get_shares_count.strip().split()[0]
    ) if (get_shares_count) else 0

    get_comments_count = "".join(
        selector.css('button.tec--btn *::text').getall()
    ).strip().split()
    comments_count = int(get_comments_count[0]) if (
        len(get_comments_count) != 0
    ) else 0

    summary = "".join(selector.css(
        'div.tec--article__body p:first-child *::text'
    ).getall())
    sources = [source.strip() for source in selector.css(
        'div.z--mb-16 div a::text'
    ).getall()]
    categories = [category.strip() for category in selector.css(
        '#js-categories a::text'
    ).getall()]
    return {
        "url": url,
        "title": title,
        "timestamp": timestamp,
        "writer": writer,
        "shares_count": shares_count,
        "comments_count": comments_count,
        "summary": summary,
        "sources": sources,
        "categories": categories
    }


# Requisito 3
def scrape_novidades(html_content):
    """Seu código deve vir aqui"""
    selector = Selector(text=html_content)
    return selector.css(
        'div.card-body p::text'
    ).getall()


# Requisito 4
def scrape_next_page_link(html_content):
    """Seu código deve vir aqui"""
    selector = Selector(text=html_content)
    return selector.css('a.tec--btn::attr(href)').get()


def fetch_via_cep(url):
    """Seu código deve vir aqui"""
    time.sleep(1)
    try:
        response = requests.get(url, timeout=3)
    except requests.Timeout:
        return '*Timeout*'
    if response.status_code == 200:
        respon_dict = response.json()
        if respon_dict.get('erro'):
            return '*erro*'
        return respon_dict['bairro']
    return '*api_erro*'
# Requisito 5
def get_tech_news(html_content):
    """Seu código deve vir aqui"""
    # html_content = fetch("https://www.ruacep.com.br/sp/sao-jose-dos-campos/bairros/")

    selector = Selector(text=html_content)
    bairro_site_list = selector.css(
        'div.card-header a strong::text'
    ).getall()
    cep_text_list = scrape_novidades(html_content)
    # union_cep_bairro = []
    # for index, bairro in (bairro_site_list):
    #     union_cep_bairro.append({ 'bairro': bairro, 'cep': cep_text_list[index] })

    result = []

    for index, cep_text in enumerate(cep_text_list):
        cep_split = cep_text.split()
        cep_1 = ''.join(cep_split[1].split('-'))
        cep_2 = ''.join(cep_split[3].split('-'))
        bairro_site = bairro_site_list[index],
        # print('bairro_site', bairro_site[0])
        bairro_via_cep_1 = fetch_via_cep(f'https://viacep.com.br/ws/{cep_1}/json/')
        bairro_via_cep_2 = fetch_via_cep(f'https://viacep.com.br/ws/{cep_2}/json/')
        dict_append = {
            'bairro_via_cep_1': bairro_via_cep_1,
            'bairro_via_cep_2': bairro_via_cep_2,
            'bairro_site_____': bairro_site[0],
            'cep_1': cep_1,
            'cep_2': cep_2
        }
        result.append(dict_append)
        # ola = cep_split[1]
        # print(ola)
    # response_cep_api = requests.get("https://viacep.com.br/ws/12232845/json/", timeout=3)
    # oi = json.load(response_cep_api)
    # print('CEP API', response_cep_api.json()['bairro'])

    return result

    # news = []

    # index = 0
    # while len(news) < amount:
    #     if index == len(links_novidades):
    #         next_page_link = scrape_next_page_link(html_content)
    #         html_content = fetch(next_page_link)
    #         links_novidades = scrape_novidades(html_content)
    #         index = 0
    #     html_content_noticia = fetch(links_novidades[index])
    #     news.append(scrape_noticia(html_content_noticia))
    #     index += 1
    # create_news(news)
    # return news

# def get_tech_news_list():
#     array_number = ['', 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
#     finish_result = []
#     for index in array_number:
#         html_content = fetch(f"https://www.ruacep.com.br/sp/sao-jose-dos-campos/bairros/{index}")
#         array_dict_get = get_tech_news(html_content)
#         finish_result.extend(array_dict_get)
#     json_str = json.dumps({'finish_result': finish_result}, indent=4, ensure_ascii=False)
#     with open("dados.json", "w") as arquivo:
#         arquivo.write(json_str)
#     return finish_result

# def analise_ceps_dados():
#     with open("dados.json", 'r') as arquivo:
#         data = json.loads(arquivo.read())
#         # print(data['finish_result'])
#         ceps = []
#         for index in data['finish_result']:
#             ceps.append({ 'bairro': index['bairro_via_cep_1']})
#     json_str = json.dumps({'bairros': ceps}, indent=4, ensure_ascii=False)
#     with open("dados_2.json", "w") as arquivo:
#         arquivo.write(json_str)
#     return ceps

def remove_space(wikpedia_list):
    bairro_wikpedia_list_filtado = []
    for bairro in wikpedia_list:
        format_bairro = bairro.replace('\n', '')
        if bairro != '\n':
            bairro_wikpedia_list_filtado.append(format_bairro)
    return bairro_wikpedia_list_filtado

def wikpedia_scrap():
    html_content = fetch("https://pt.wikipedia.org/wiki/Lista_de_bairros_de_S%C3%A3o_Jos%C3%A9_dos_Campos#:~:text=Possui%2073%20bairros.,3%2C38%20hab%2Fres.")

    selector = Selector(text=html_content)
    bairro_wikpedia_list = selector.css(
        'table.wikitable tbody tr th *::text'
    ).getall()[3:]
    zona_wikpedia_list = selector.css(
        'table.wikitable tbody tr td[align="center"] *::text'
    ).getall()
    
    bairro_list = remove_space(bairro_wikpedia_list)
    zona_list = remove_space(zona_wikpedia_list)
    print('len(bairro_list)', len(bairro_list))
    print('len(zona_list)', len(zona_list))

    bairro_zona_wikpedia_list = []
    boll = True
    for index, bairro in enumerate(bairro_list):
        if bairro == 'Jardim São José':
            boll = False
        elif boll:
            bairro_zona_wikpedia_list.append({ 'bairro': bairro, 'zona': zona_list[index] })
        else:
            bairro_zona_wikpedia_list.append({ 'bairro': bairro, 'zona': zona_list[index+1] })

    # with open("dados_2.json", 'r') as arquivo:
    #     data = json.loads(arquivo.read())
    #     for index in data['ceps']:
    #         print()
    json_str = json.dumps({'bairro_zona': bairro_zona_wikpedia_list}, indent=4, ensure_ascii=False)
    with open("dados_3.json", "w") as arquivo:
        arquivo.write(json_str)
    return bairro_zona_wikpedia_list
# Jardim São José, É o problema

print(wikpedia_scrap())
