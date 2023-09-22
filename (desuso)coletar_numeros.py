import json
import re
from playwright.sync_api import sync_playwright
from time import sleep
from pathlib import Path

todas_cidades = []
uf_estados = json.loads(open('uf_estados.json').read())
acompanhantes = []


def quantidade_numeros():
    with open('telefones.txt') as f:
        return len(f.readlines())


def filtrar_cidades_por_uf(uf):
    
        with open(f"cidades/{uf_estados[uf]}") as f:
            link = json.load(f)
            for url in link['links']:
                if re.search('acompanhantes', url):
                    todas_cidades.append(url)
                    print(url)

def filtrar_tudo():
    
    for uf in uf_estados.keys():
        filtrar_cidades_por_uf(uf)
        


def buscar_numeros():
    # APAGARÁ O ARQUIVO TELEFONES SEMPRE QUE A FUNÇÃO FOR INVOCADA
    path = Path('telefones.txt')
    if path.exists():
        path.unlink()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
        context = browser.new_context(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/000000000 Safari/537.36')
        page = context.new_page()
        for cidade in todas_cidades:
            
            page.goto(cidade)
            try:
                page.wait_for_selector('xpath=/html/body/div[2]/div[1]/div/div/section/div/button', timeout=3000).click()
            except:
                pass
            if 'Ainda não há acompanhantes nesta cidade' in page.inner_text('body'):
                print('Não há acompanhantes nesta cidade')
            else:
                links = page.query_selector_all('a')
                    
                for link in links:
                        # Inicializa 'valido' como False a cada iteração
                        valido = False
                            
                            # Validando Acompanhante para extrair contato
                        href = link.get_attribute("href")
                        if href:
                            valido = bool(re.search(r'-\d+$', href))

                        if valido:
                            sleep(0.5)
                            print(f'Acompanhante encontrado: {href}')
                            if href not in acompanhantes:
                                acompanhantes.append(href)
                for acompanhante in acompanhantes: 
                    page2 = context.new_page()
                    page2.goto(acompanhante)
                    
                    if 'Tenha acesso ao número de telefone desse e outros perfis no ' in page2.content():
                        print('Numero Bloqueado')
                        page2.close()
                        continue
            
                    else:
                            
                            telefone = re.findall(r'\(\d{2}\) \d{5}-\d{4}',page2.content())
                            telefone = ''.join(telefone)
                            telefone = str(telefone)
                            telefone = telefone.replace('(', '') 
                            telefone = telefone.replace(')', '')
                            telefone = telefone.replace('-', '')
                            telefone = telefone.replace(' ', '')
                            telefone = '+55' + telefone
                            with open('telefones.txt', 'a') as f:
                                f.write(telefone[0:13] + '\n')
                                #Numeros secundarios
                               # if len(telefone) > 13:
                                   # f.write(telefone[14:] + '\n')
                                #print(telefone[14:])
                                print(telefone[0:13])
                            
                         
                            page2.close()


if __name__ == '__main__':
    #filtrar_tudo()
    #coletar()
    print( quantidade_numeros())