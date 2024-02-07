import requests
from bs4 import BeautifulSoup as BS


async def get_sovmest(z_m, z_w, type) -> list:
    v = []
    r = requests.get(f'https://horoscopes.rambler.ru/sovmestimost-znakov-zodiaka/zhenshhina-{z_w}-muzhchina-{z_m}/')
    if r.status_code != 200:
        print(r.status_code)
        return v

    soup = BS(r.content, 'html.parser')
    predislov = soup.find('p', class_='mtZOt').text.strip()  # good
    v.append(predislov)
    all = soup.find('div', class_='_1E4Zo _3BLIa').find_all(['p', 'h2'])
    index = 0
    for i, content in enumerate(all):
        if content.text == type:
            index = i
            v.append(content.text)
            break

    for i in all[index + 1:]:
        if i.name == 'h2':
            break
        v.append(i.text)
    return v
