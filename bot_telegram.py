import telebot
from telebot import types
from async_coletar_numeros import  quantidade_numeros, filtrar_cidades_por_uf, buscar_numeros, filtrar_tudo
from datetime import datetime
import asyncio
from telebot.async_telebot import AsyncTeleBot
from playwright.async_api import async_playwright

respostas = {}
token = '6005438493:AAHXK_ssUTXDZ8e6N4dlp2Yk37l1VthRRCg'
admins = ['rafaellima777']
bot = AsyncTeleBot(token)

estado = None
CHAT_ID = None
ADMIN = False
DATA = None
@bot.message_handler(commands=['start'])

async def start(message):
    global ADMIN
    for adm in admins:
        if message.chat.username == adm:
            ADMIN = True
    if ADMIN: 

        await bot.send_message(message.chat.id, '''
Digite /coletar  para iniciar a coleta de números no no Fatal Model\n
Digite /whatsapp Para autenticar o seu whatsapp ao servidor para disparar mensagens\n
Digite /usuario para permitir que outro usuario use o bot\n
Digite /numeros para ver quantos números foram coletados\n
        
''')
    else:
       await bot.send_message(message.chat.id, 'Vocë não tem permissão para usar esse comando')



@bot.message_handler(commands=['coletar'])        
async def coletar(message):
    global ADMIN
    global DATA
    menu = types.InlineKeyboardMarkup(row_width=4)
    menu.add(types.InlineKeyboardButton('SP', callback_data='sp'))
    menu.add(types.InlineKeyboardButton('RJ', callback_data='rj'))
    menu.add(types.InlineKeyboardButton('MG', callback_data='mg'))
    menu.add(types.InlineKeyboardButton('BA', callback_data='ba'))
    menu.add(types.InlineKeyboardButton('PR', callback_data='pr'))
    menu.add(types.InlineKeyboardButton('MS', callback_data='ms'))
    menu.add(types.InlineKeyboardButton('ES', callback_data='es'))
    menu.add(types.InlineKeyboardButton('GO', callback_data='go'))
    menu.add(types.InlineKeyboardButton('MT', callback_data='mt'))
    menu.add(types.InlineKeyboardButton('SC', callback_data='sc'))
    menu.add(types.InlineKeyboardButton('Todos', callback_data='todos'))
    if ADMIN:
        await bot.send_message(message.chat.id, f'Ultima Coleta: {DATA}')
        await bot.send_message(message.chat.id, 'Me informe um estado:', reply_markup=menu)
    else:
        await bot.send_message(message.chat.id, 'Vocë não tem permissão para usar esse comando')


@bot.message_handler(commands=['whatsapp'])
async def whatsapp(message):
    if ADMIN:
        mensagem = '&text=%F0%9F%8F%98%EF%B8%8FCASA%20PARA%20ATENDIMENTO%20E%20HOSPEDAGEM%0APOUSO%20ALEGRE%20-%20MG%0A%F0%9F%8C%9FNOVO%20LOCAL%F0%9F%8C%9F%0A%0A%F0%9F%9B%8E%EF%B8%8FTrabalhe%20%C3%A0%20vontade%2C%20aqui%20voc%C3%AA%20pode%20fazer%20seu%20Atendimento%2024hs%2C%20prezamos%20por%20discri%C3%A7%C3%A3o.%0A%F0%9F%8C%9FNOVISSIMO%20LOCAL%20NO%20CENTRO%F0%9F%8C%9F%0A%F0%9F%8E%A5%20C%C3%A2meras%20de%20Seguran%C3%A7a%2024%20hs%0AN%C3%83O%20COBRAMOS%20NENHUMA%20TAXA%20DE%20SERVI%C3%87O%0A%0A%F0%9F%9B%8C2%20Quartos%20%7C%20%F0%9F%9B%8C%20%F0%9F%9A%BF2%20Su%C3%ADtes%0A%F0%9F%8C%AC%EF%B8%8FVentiladores%20%7C%20%F0%9F%93%B6%20%F0%9F%93%B2%20Wi-fi%20%7C%20%F0%9F%93%9AToalhas%2C%20Len%C3%A7%C3%B3is%2C%20fronhas%2C%20travesseiros%2C%20mantas%20NOVOS%0A%F0%9F%8E%9B%EF%B8%8F%20Fog%C3%A3o%2C%20Microondas%20%7C%20%F0%9F%A7%8A%20Geladeira%20%7C%20%F0%9F%8D%BD%EF%B8%8F%20Utens%C3%ADlios%20dom%C3%A9sticos%0A%0A%F0%9F%A6%B1%F0%9F%91%97%F0%9F%91%99%20M%C3%81QUINA%20DE%20LAVAR%20Tanque%20e%20%C3%81rea%20de%20Servi%C3%A7o%0A%F0%9F%A6%B3%F0%9F%A7%BD%20Produtos%20de%20limpeza%20de%20%C3%A1rea%20comum%0A%F0%9F%9A%AC%20%C3%81rea%20para%20fumantes%20-%20(somente%20para%20o%20Hospede)%0A%0ADi%C3%A1ria%0A%F0%9F%92%B0100%20quartos.%0A%F0%9F%92%B0130%20su%C3%ADtes.%0A%0APara%20reservar%20chame%20Alexandre%20pelo%20n%C3%BAmero%3A%0A22992858008'
        link = 'https://web.whatsapp.com/send?phone='
        numeros = []
        with open('numeros.txt', 'r') as f:
            numero = f.readlines()
        for i in numero:
            if len(i) > 10:
        
                formatado = i.strip().replace('\n', '')
                numeros.append(formatado)



        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36')
            page = await context.new_page()
            await page.goto('https://web.whatsapp.com/')
            scan = False
            while not scan:
                qrcode = await page.query_selector('canvas')
                if qrcode:
                    await qrcode.screenshot(path='whatsapp.png')
                    await bot.send_message(message.chat.id, text='Acesse: hyttp://18.196.23.184/qrcode.html, em outro dispositivo, para vincular o seu whatsapp')
                    print('QRcode Salvo')
                    await asyncio.sleep(21)
                    
                    botao_inicio = await page.wait_for_selector('xpath=/html/body/div[1]/div/div/div[4]/header/div[2]/div/span/div[4]/div/span', timeout=600000)
                    if botao_inicio:
                        scan = True
                        break
                    
                    reload = await page.query_selector('[role="button"][name="refresh-l-light Click to reload QR code"]')
                    if reload:
                        await reload.click()
                        
            
            await bot.send_message(message.chat.id, 'Seu whatsapp foi vinculado com sucesso, vamos iniciar o envio em massa')
            for i in numeros:
                await page.goto(f'{link}{i}{mensagem}')
                botao_enviar = await page.wait_for_selector("xpath=/html/body/div[1]/div/div/div[5]/div/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span",timeout=2000000)
                await botao_enviar.click()
                await asyncio.sleep(10)
                #outra mensagem para o bot aqui
                await bot.send_message(message.chat.id, f'enviando para {i}')
                
                await asyncio.sleep(20)
        #await browser.close()
        
    else:
        await bot.send_message(message.chat.id, 'Vocë não tem permissão para usar esse comando')

@bot.message_handler(commands=['usuario'])
async def usuario(message):
    if ADMIN:
        await bot.send_message(message.chat.id, 'Digite o nome de usuário que deseja dar acesso')
        await bot.register_next_step_handler(message, adicionar)
    else:
        await bot.send_message(message.chat.id, 'Vocë não tem permissão para usar esse comando')
        
async def adicionar(message):
    usuario = message.text
    admins.append(usuario)
    await bot.send_message(message.chat.id, 'Usuário adicionado com sucesso')
    await bot.send_message(message.chat.id, f'Usuarios com acesso: {",  ".join(admins)}')

@bot.message_handler(commands=['numeros'])
async def numeros(message):
    if ADMIN:
        with open('telefones.txt', 'r') as f:
            numeros = len(f.readlines())
            await bot.send_message(message.chat.id, f'Estamos com: {numeros} numeros armazenados')
    else:
        await bot.send_message(message.chat.id, 'Você não tem permissões para fazer isso')        


@bot.callback_query_handler(func=lambda call: True)
async def handle_query(call):
    if call.data == "sp":
        global DATA
        await bot.send_message(call.message.chat.id, "Ok, Vamos coletar todos os numeros do estado de SP, isso vai demorar um tempo, mas eu aviso quando acabar")
        data_coleta = datetime.now()
        DATA = data_coleta.strftime("%d/%m/%Y - %H:%M:%S")
        await filtrar_cidades_por_uf('sp')
        await buscar_numeros()
        final = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
        await bot.send_message(call.message.chat.id, f"Fim da coleta: {final}")
        await bot.send_message(call.message.chat.id, f"Coletamos {quantidade_numeros()} números")
        
    elif call.data == "rj":
        
        await bot.send_message(call.message.chat.id, "Ok, Vamos coletar todos os numeros do estado de RJ, isso vai demorar um tempo, mas eu aviso quando acabar")
        data_coleta = datetime.now()
        DATA = data_coleta.strftime("%d/%m/%Y - %H:%M:%S")
        await filtrar_cidades_por_uf('rj')
        await buscar_numeros()
        final = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
        await bot.send_message(call.message.chat.id, f"Fim da coleta: {final}")
        await bot.send_message(call.message.chat.id, f"Coletamos {quantidade_numeros()} números")

    elif call.data == "mg":
        await bot.send_message(call.message.chat.id, "Ok, Vamos coletar todos os numeros do estado de MG, isso vai demorar um tempo, mas eu aviso quando acabar")
        data_coleta = datetime.now()
        DATA = data_coleta.strftime("%d/%m/%Y - %H:%M:%S")
        filtrar_cidades_por_uf('mg')
        await buscar_numeros()
        final = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
        await bot.send_message(call.message.chat.id, f"Fim da coleta: {final}")
        await bot.send_message(call.message.chat.id, f"Coletamos {quantidade_numeros()} números")

    elif call.data == "ba":
        #global DATA
        await bot.send_message(call.message.chat.id, "Ok, Vamos coletar todos os numeros do estado de BA, isso vai demorar um tempo, mas eu aviso quando acabar")
        await filtrar_cidades_por_uf('ba')
        data_coleta = datetime.now()
        DATA = data_coleta.strftime("%d/%m/%Y - %H:%M:%S")
        await buscar_numeros()
        final = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
        await bot.send_message(call.message.chat.id, f"Fim da coleta: {final}")
        await bot.send_message(call.message.chat.id, f"Coletamos {quantidade_numeros()} números")

    elif call.data == "pr":
        #global DATA
        await bot.send_message(call.message.chat.id, "Ok, Vamos coletar todos os numeros do estado de PR, isso vai demorar um tempo, mas eu aviso quando acabar")
        await filtrar_cidades_por_uf('pr')
        data_coleta = datetime.now()
        DATA = data_coleta.strftime("%d/%m/%Y - %H:%M:%S")
        await buscar_numeros()
        final = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
        await bot.send_message(call.message.chat.id, f"Fim da coleta: {final}")
        await bot.send_message(call.message.chat.id, f"Coletamos {quantidade_numeros()} números")
    
    elif call.data == "ms":
        #global DATA
        await bot.send_message(call.message.chat.id, "Ok, Vamos coletar todos os numeros do estado de MS, isso vai demorar um tempo, mas eu aviso quando acabar")
        await filtrar_cidades_por_uf('ms')
        data_coleta = datetime.now()
        DATA = data_coleta.strftime("%d/%m/%Y - %H:%M:%S")
        await buscar_numeros()
        final = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
        await bot.send_message(call.message.chat.id, f'Fim da coleta: {final}')
        await bot.send_message(call.message.chat.id, f"Coletamos {quantidade_numeros()} números")
    
    elif call.data == "es":
        #global DATA
        await bot.send_message(call.message.chat.id, "Ok, Vamos coletar todos os numeros do estado de ES, isso vai demorar um tempo, mas eu aviso quando acabar")
        await filtrar_cidades_por_uf('es')
        data_coleta = datetime.now()
        DATA = data_coleta.strftime("%d/%m/%Y - %H:%M:%S")
        await buscar_numeros()
        final = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
        await bot.send_message(call.message.chat.id, f'Fim da coleta: {final}')
        await bot.send_message(call.message.chat.id, f"Coletamos {quantidade_numeros()} números")
        
    
    elif call.data == 'sc':
        #global DATA 
        data_coleta = datetime.now()
        DATA = data_coleta.strftime("%d/%m/%Y - %H:%M:%S")
        await bot.send_message(call.message.chat.id, "Ok, Vamos coletar todos os numeros do estado de SC, isso vai demorar um tempo, mas eu aviso quando acabar")
        await filtrar_cidades_por_uf('sc')
        await buscar_numeros()
        final = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
        await bot.send_message(call.message.chat.id, f"Fim da coleta: {final}")
        await bot.send_message(call.message.chat.id, f"Coletamos {quantidade_numeros()} números")
    
    elif call.data == 'go':
        bot.send_message(call.message.chat.id, "Ok, Vamos coletar todos os numeros do estado de GO, isso vai demorar um tempo, mas eu aviso quando acabar")
        filtrar_cidades_por_uf('go')
        buscar_numeros()
        bot.send_message(call.message.chat.id, "Fim da coleta")
        bot.send_message(call.message.chat.id, f"Coletamos {quantidade_numeros()} números")

    elif call.data == 'mt':
        #global DATA
        data_coleta = datetime.now()
        await bot.send_message(call.message.chat.id, "Ok, Vamos coletar todos os numeros do estado de MT, isso vai demorar um tempo, mas eu aviso quando acabar")
        await filtrar_cidades_por_uf('mt')
        DATA = data_coleta.strftime("%d/%m/%Y - %H:%M:%S")
        await buscar_numeros()
        final = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
        await bot.send_message(call.message.chat.id, f"Fim da coleta: {final}")
        await bot.send_message(call.message.chat.id, f"Coletamos {quantidade_numeros()} números")
        
    elif call.data == 'todos':
        #global DATA
        await bot.send_message(call.message.chat.id, "Ok, Vamos coletar todos os numeros do estado de SP, isso vai demorar um tempo, mas eu aviso quando acabar")
        DATA = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
        await filtrar_tudo()
        await buscar_numeros()
        final = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
        await bot.send_message(call.message.chat.id, f"Fim da coleta: {final}")
        await bot.send_message(call.message.chat.id, f"Coletamos {quantidade_numeros()} números")

async def main():
    while True:
        try: 
            await bot.polling(none_stop=True)
        except Exception as e:
            print(f'Erro: {e}, reconectando...')
            await asyncio.sleep(5)
if __name__ == '__main__':
    asyncio.run(main())