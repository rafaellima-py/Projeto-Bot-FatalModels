import json
import re
import aiofiles
from playwright.async_api import async_playwright
from time import sleep
from pathlib import Path
import asyncio
from time import sleep
todas_cidades = []
uf_estados = json.loads(open('uf_estados.json').read())
acompanhantes = []


async def quantidade_numeros():
     async with aiofiles.open('telefones.txt', mode='r') as f:
         content = await f.read()
         return content


async def filtrar_cidades_por_uf(uf):
    
         async with aiofiles.open(f"cidades/{uf_estados[uf]}",mode='r') as f:
            content = await f.read()
            link = json.loads(content)
            #link = await json.load(f)
            for url in link['links']:
                if re.search('acompanhantes', url):
                    todas_cidades.append(url)
                    print(url)

async def filtrar_tudo():
    
    for uf in uf_estados.keys():
        await filtrar_cidades_por_uf(uf)
        


async def buscar_numeros():
    # APAGARÁ O ARQUIVO TELEFONES SEMPRE QUE A FUNÇÃO FOR INVOCADA
    path = Path('telefones.txt')
    if path.exists():
        path.unlink()

    async with async_playwright() as p:
        browser =  await p.chromium.launch(headless=False, args=['--no-sandbox', '--disable-setuid-sandbox'])
        context =  await browser.new_context(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/000000000 Safari/537.36')
        page = await context.new_page()
        
        for cidade in todas_cidades:
            
            await page.goto(cidade)
            try:
                botao = await page.wait_for_selector('xpath=/html/body/div[2]/div[1]/div/div/section/div/button', timeout=3000)
                await botao.click()
            except:
                pass
            inner_text = await page.inner_text('body')
            if 'Ainda não há acompanhantes nesta cidade' in inner_text:
                print('Não há acompanhantes nesta cidade')
            else:
                links = await page.query_selector_all('a')
                    
                for link in links:
                        # Inicializa 'valido' como False a cada iteração
                        valido = False
                            
                            # Validando Acompanhante para extrair contato
                        href = await link.get_attribute("href")
                        if href:
                            valido = bool(re.search(r'-\d+$', href))

                        
                        if valido:
                            print(f'Acompanhante encontrado: {href}')
                            if href not in acompanhantes:
                                acompanhantes.append(href)
                for acompanhante in acompanhantes:
                     
                    page2 = await context.new_page()
                    try:
                        await page2.goto(acompanhante, timeout=80000)
                    except:
                        continue
                    content_p2 = await page2.content()
                    if 'Tenha acesso ao número de telefone desse e outros perfis no ' in content_p2:
                        print('Numero Bloqueado')
                        await page2.close()
                        continue
            
                    else:
                            
                            telefone = re.findall(r'\(\d{2}\) \d{5}-\d{4}',await page2.content())
                            telefone = ''.join(telefone)
                            telefone = str(telefone)
                            telefone = telefone.replace('(', '') 
                            telefone = telefone.replace(')', '')
                            telefone = telefone.replace('-', '')
                            telefone = telefone.replace(' ', '')
                            telefone = '+55' + telefone
                            async with aiofiles.open('telefones.txt', mode='a') as f:
                                await f.write(telefone[0:13] + '\n')
                                
                                #Numeros secundarios
                               # if len(telefone) > 13:
                                   # f.write(telefone[14:] + '\n')
                                #print(telefone[14:])
                                print(telefone[0:13])
                            
                         
                            await page2.close()


async def main():
    await filtrar_tudo()
    await buscar_numeros()

if __name__ == '__main__':

    asyncio.run(main())