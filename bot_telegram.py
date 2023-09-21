from telebot import TeleBot
from telebot import types
from coletar_numeros import  quantidade_numeros, filtrar_cidades_por_uf, buscar_numeros, filtrar_tudo
from datetime import datetime

respostas = {}

admins = ['rafaellima777']
bot = TeleBot(token)
estado = None
ADMIN = False
DATA = None
@bot.message_handler(commands=['start'])

def start(message):
    global ADMIN
    for adm in admins:
        if message.chat.username == adm:
            ADMIN = True
    if ADMIN: 
        bot.send_message(message.chat.id, '''
        Digite /coletar  para iniciar a coleta de números no no Fatal Model\n
Digite /whatsapp Para autenticar o seu whatsapp ao servidor para disparar mensagens\n
Digite /usuario para permitir que outro usuario use o bot\n
Digite /numeros para ver quantos números foram coletados\n
        
*Nota:* A função /whatsapp está em desenvolvimento, mas você pode usar o App desktop para disparar mensagens               
                        ''')
    else:
        bot.send_message(message.chat.id, 'Vocë não tem permissão para usar esse comando')



@bot.message_handler(commands=['coletar'])        
def coletar(message):
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
        bot.send_message(message.chat.id, f'Ultima Coleta: {DATA}')
        bot.send_message(message.chat.id, 'Me informe um estado:', reply_markup=menu)
    else:
        bot.send_message(message.chat.id, 'Vocë não tem permissão para usar esse comando')

@bot.message_handler(commands=['usuario'])
def usuario(message):
    if ADMIN:
        bot.send_message(message.chat.id, 'Digite o nome de usuário que deseja dar acesso')
        bot.register_next_step_handler(message, adicionar)
    else:
        bot.send_message(message.chat.id, 'Vocë não tem permissão para usar esse comando')
        
def adicionar(message):
    usuario = message.text
    admins.append(usuario)
    bot.send_message(message.chat.id, 'Usuário adicionado com sucesso')
    bot.send_message(message.chat.id, f'Usuarios com acesso: {",  ".join(admins)}')

@bot.message_handler(commands=['numeros'])
def numeros(message):
    if ADMIN:
        with open('telefones.txt', 'r') as f:
            numeros = len(f.readlines())
            bot.send_message(message.chat.id, f'Estamos com: {numeros} numeros armazenados')
    else:
        bot.send_message(message.chat.id, 'Você não tem permissões para fazer isso')        


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == "sp":
        bot.send_message(call.message.chat.id, "Ok, Vamos coletar todos os numeros do estado de SP, isso vai demorar um tempo, mas eu aviso quando acabar")
        filtrar_cidades_por_uf('sp')
        buscar_numeros()
        bot.send_message(call.message.chat.id, "Fim da coleta")
        bot.send_message(call.message.chat.id, f"Coletamos {quantidade_numeros()} números")
        
    elif call.data == "rj":
        global DATA
        bot.send_message(call.message.chat.id, "Ok, Vamos coletar todos os numeros do estado de RJ, isso vai demorar um tempo, mas eu aviso quando acabar")
        data_coleta = datetime.now()
        DATA = data_coleta.strftime("%d/%m/%Y - %H:%M:%S")
        filtrar_cidades_por_uf('rj')
        buscar_numeros()
        final = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
        bot.send_message(call.message.chat.id, f"Fim da coleta: {final}")
        bot.send_message(call.message.chat.id, f"Coletamos {quantidade_numeros()} números")

    elif call.data == "mg":
        bot.send_message(call.message.chat.id, "Ok, Vamos coletar todos os numeros do estado de MG, isso vai demorar um tempo, mas eu aviso quando acabar")
        data_coleta = datetime.now()
        DATA = data_coleta.strftime("%d/%m/%Y - %H:%M:%S")
        filtrar_cidades_por_uf('mg')
        buscar_numeros()
        final = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
        bot.send_message(call.message.chat.id, f"Fim da coleta: {final}")
        bot.send_message(call.message.chat.id, f"Coletamos {quantidade_numeros()} números")

    elif call.data == "ba":
        #global DATA
        bot.send_message(call.message.chat.id, "Ok, Vamos coletar todos os numeros do estado de BA, isso vai demorar um tempo, mas eu aviso quando acabar")
        filtrar_cidades_por_uf('ba')
        data_coleta = datetime.now()
        DATA = data_coleta.strftime("%d/%m/%Y - %H:%M:%S")
        buscar_numeros()
        final = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
        bot.send_message(call.message.chat.id, f"Fim da coleta: {final}")
        bot.send_message(call.message.chat.id, f"Coletamos {quantidade_numeros()} números")

    elif call.data == "pr":
        #global DATA
        bot.send_message(call.message.chat.id, "Ok, Vamos coletar todos os numeros do estado de PR, isso vai demorar um tempo, mas eu aviso quando acabar")
        filtrar_cidades_por_uf('pr')
        data_coleta = datetime.now()
        DATA = data_coleta.strftime("%d/%m/%Y - %H:%M:%S")
        buscar_numeros()
        final = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
        bot.send_message(call.message.chat.id, f"Fim da coleta: {final}")
        bot.send_message(call.message.chat.id, f"Coletamos {quantidade_numeros()} números")
    
    elif call.data == "ms":
        #global DATA
        bot.send_message(call.message.chat.id, "Ok, Vamos coletar todos os numeros do estado de MS, isso vai demorar um tempo, mas eu aviso quando acabar")
        filtrar_cidades_por_uf('ms')
        data_coleta = datetime.now()
        DATA = data_coleta.strftime("%d/%m/%Y - %H:%M:%S")
        buscar_numeros()
        final = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
        bot.send_message(call.message.chat.id, f'Fim da coleta: {final}')
        bot.send_message(call.message.chat.id, f"Coletamos {quantidade_numeros()} números")
    
    elif call.data == "es":
        #global DATA
        bot.send_message(call.message.chat.id, "Ok, Vamos coletar todos os numeros do estado de ES, isso vai demorar um tempo, mas eu aviso quando acabar")
        filtrar_cidades_por_uf('es')
        data_coleta = datetime.now()
        DATA = data_coleta.strftime("%d/%m/%Y - %H:%M:%S")
        buscar_numeros()
        final = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
        bot.send_message(call.message.chat.id, f'Fim da coleta: {final}')
        bot.send_message(call.message.chat.id, f"Coletamos {quantidade_numeros()} números")
        
    
    elif call.data == 'sc':
        #global DATA 
        data_coleta = datetime.now()
        DATA = data_coleta.strftime("%d/%m/%Y - %H:%M:%S")
        bot.send_message(call.message.chat.id, "Ok, Vamos coletar todos os numeros do estado de SC, isso vai demorar um tempo, mas eu aviso quando acabar")
        filtrar_cidades_por_uf('sc')
        buscar_numeros()
        final = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
        bot.send_message(call.message.chat.id, f"Fim da coleta: {final}")
        bot.send_message(call.message.chat.id, f"Coletamos {quantidade_numeros()} números")
    
    elif call.data == 'go':
        bot.send_message(call.message.chat.id, "Ok, Vamos coletar todos os numeros do estado de GO, isso vai demorar um tempo, mas eu aviso quando acabar")
        filtrar_cidades_por_uf('go')
        buscar_numeros()
        bot.send_message(call.message.chat.id, "Fim da coleta")
        bot.send_message(call.message.chat.id, f"Coletamos {quantidade_numeros()} números")

    elif call.data == 'mt':
        #global DATA
        data_coleta = datetime.now()
        bot.send_message(call.message.chat.id, "Ok, Vamos coletar todos os numeros do estado de MT, isso vai demorar um tempo, mas eu aviso quando acabar")
        filtrar_cidades_por_uf('mt')
        DATA = data_coleta.strftime("%d/%m/%Y - %H:%M:%S")
        buscar_numeros()
        final = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
        bot.send_message(call.message.chat.id, f"Fim da coleta: {final}")
        bot.send_message(call.message.chat.id, f"Coletamos {quantidade_numeros()} números")
        
    elif call.data == 'todos':
        #global DATA
        bot.send_message(call.message.chat.id, "Ok, Vamos coletar todos os numeros do estado de SP, isso vai demorar um tempo, mas eu aviso quando acabar")
        DATA = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
        filtrar_tudo()
        buscar_numeros()
        final = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
        bot.send_message(call.message.chat.id, f"Fim da coleta: {final}")
        bot.send_message(call.message.chat.id, f"Coletamos {quantidade_numeros()} números")







bot.polling()