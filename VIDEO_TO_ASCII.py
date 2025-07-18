import cv2
import curses
import locale
locale.setlocale(locale.LC_ALL, '')


cor = False
tipo = False
sair = False


tam = 63



def check_config():
        global ascii_chars
        if tipo:
            ascii_chars = ["█", "▓", "▒", "░", "▉", "▊", "▋", "▌", "▍", "▎", "▏", "▐", "▄", "▁", "▂", "▃", "▅", "▆", "▇", " "]

        if not tipo:
            ascii_chars = "@%#*+=-:. "
        return
        


def check_click(key):
    global sair, cor, tipo
    if key == ord('q'):
        sair = True
    elif key == ord('c'):
        cor = not cor
    if key == ord('t'):
        tipo = not tipo
    return

text_box = [
    {"x": 0, "y": 70, "content": "pressione 'q' para sair", "color_pair": 1},
    {"x": 1, "y": 70, "content": "pressione 'c' para trocar de cor", "color_pair": 1},
    {"x": 2, "y": 70, "content": "pressione 't' para mudar o tipo", "color_pair": 1},
]



def imagem_para_ascii(win):
    global ascii_img

    video = cv2.VideoCapture(0)

    while not sair:
        ascii_img = ""
        check_config()
        ok, frame = video.read()
        inv_frame = cv2.flip(frame, 1)
        if not ok:
            print("\033[31mERRO AO ACESSAR VIDEO!!!\033[0m")
            break

        imagem = cv2.cvtColor(inv_frame, cv2.COLOR_BGR2GRAY)
        altura = int(tam * 0.55)
        resize = cv2.resize(imagem, (tam, altura), interpolation=cv2.INTER_CUBIC)

        for row in resize:
            for pixel in row:
                ascii_img += ascii_chars[int((len(ascii_chars) - 1) * int(pixel) // 255)]
            ascii_img += '\n'

        win.clear()
        
        win.addstr(0, 0, ascii_img, curses.color_pair(1 if cor else 2))

        for parameter in text_box:
            win.addstr(parameter["x"] , parameter["y"], parameter["content"], parameter["color_pair"])

        key = win.getch()
        check_click(key)
        win.refresh()
    video.release()

def main(stdscr):
    curses.start_color()
    
    curses.init_pair(1,curses.COLOR_MAGENTA,curses.COLOR_WHITE)
    curses.init_pair(2,curses.COLOR_BLACK,curses.COLOR_WHITE)
    curses.curs_set(0)
    stdscr.nodelay(True)
    
    imagem_para_ascii(stdscr)

curses.wrapper(main)
