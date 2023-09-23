from playwright.async_api import async_playwright
import asyncio
from bot_telegram import *

mensagem = '&text=%F0%9F%8F%98%EF%B8%8FCASA%20PARA%20ATENDIMENTO%20E%20HOSPEDAGEM%0APOUSO%20ALEGRE%20-%20MG%0A%F0%9F%8C%9FNOVO%20LOCAL%F0%9F%8C%9F%0A%0A%F0%9F%9B%8E%EF%B8%8FTrabalhe%20%C3%A0%20vontade%2C%20aqui%20voc%C3%AA%20pode%20fazer%20seu%20Atendimento%2024hs%2C%20prezamos%20por%20discri%C3%A7%C3%A3o.%0A%F0%9F%8C%9FNOVISSIMO%20LOCAL%20NO%20CENTRO%F0%9F%8C%9F%0A%F0%9F%8E%A5%20C%C3%A2meras%20de%20Seguran%C3%A7a%2024%20hs%0AN%C3%83O%20COBRAMOS%20NENHUMA%20TAXA%20DE%20SERVI%C3%87O%0A%0A%F0%9F%9B%8C2%20Quartos%20%7C%20%F0%9F%9B%8C%20%F0%9F%9A%BF2%20Su%C3%ADtes%0A%F0%9F%8C%AC%EF%B8%8FVentiladores%20%7C%20%F0%9F%93%B6%20%F0%9F%93%B2%20Wi-fi%20%7C%20%F0%9F%93%9AToalhas%2C%20Len%C3%A7%C3%B3is%2C%20fronhas%2C%20travesseiros%2C%20mantas%20NOVOS%0A%F0%9F%8E%9B%EF%B8%8F%20Fog%C3%A3o%2C%20Microondas%20%7C%20%F0%9F%A7%8A%20Geladeira%20%7C%20%F0%9F%8D%BD%EF%B8%8F%20Utens%C3%ADlios%20dom%C3%A9sticos%0A%0A%F0%9F%A6%B1%F0%9F%91%97%F0%9F%91%99%20M%C3%81QUINA%20DE%20LAVAR%20Tanque%20e%20%C3%81rea%20de%20Servi%C3%A7o%0A%F0%9F%A6%B3%F0%9F%A7%BD%20Produtos%20de%20limpeza%20de%20%C3%A1rea%20comum%0A%F0%9F%9A%AC%20%C3%81rea%20para%20fumantes%20-%20(somente%20para%20o%20Hospede)%0A%0ADi%C3%A1ria%0A%F0%9F%92%B0100%20quartos.%0A%F0%9F%92%B0130%20su%C3%ADtes.%0A%0APara%20reservar%20chame%20Alexandre%20pelo%20n%C3%BAmero%3A%0A22992858008'
link = 'https://web.whatsapp.com/send?phone='
numeros = []
with open('numeros_teste.txt', 'r') as f:
    numero = f.readlines()
    for i in numero:
        if len(i) > 10:
        
            formatado = i.strip().replace('\n', '')
            numeros.append(formatado)



async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto('https://web.whatsapp.com/')
        scan = False
        while not scan:
            qrcode = await page.query_selector('canvas')
            if qrcode:
                await qrcode.screenshot(path='whatsapp.png')
                bot.send_message(chat_id=CHAT_ID, text='Acesse: hyttp://18.196.23.184/qrcode.html, em outro dispositivo, para vincular o seu whatsapp')
                print('QRcode Salvo')
                await asyncio.sleep(21)
                
                botao_inicio = await page.query_selector('xpath=/html/body/div[1]/div/div/div[4]/header/div[2]/div/span/div[4]/div/span')
                if botao_inicio:
                    scan = True
                    break
                
                reload = await page.query_selector('[role="button"][name="refresh-l-light Click to reload QR code"]')
                if reload:
                    await reload.click()
                    
        #Gostaria de enviar uma mensagem atraves do bot do telegram aqui
        
        for i in numeros:
            await page.goto(f'{link}{i}{mensagem}')
            botao_enviar = await page.wait_for_selector("xpath=/html/body/div[1]/div/div/div[5]/div/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span",timeout=20000)
            await botao_enviar.click()
            await asyncio.sleep(10)
            #outra mensagem para o bot aqui
            print(f'enviando para {i}')
            
        #await asyncio.sleep(20)
        #await browser.close()

asyncio.run(main())
