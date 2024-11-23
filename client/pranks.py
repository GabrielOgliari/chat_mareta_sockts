import time
from pynput.mouse import Controller, Listener
import pyautogui
from PIL import Image
from PIL import ImageTk
import tkinter as tk
import pygame
import platform
import subprocess
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import random
import os






class Pranks:
    def __init__(self, data):
        self.prank_type = data
        self.prank_control()

    def prank_control(self ):
        match self.prank_type:
            case 'invert mouse':
                self.invert_mouse()
            case 'invert screen':
                self.invert_screen()
            case 'fright':
                self.fright()
            case 'move mouse randomly':
                self.move_mouse_randomly()

    def invert_mouse(self):
        mouse = Controller()

        start_time = time.time()
        duration = 60  # 1 minuto

        def on_move(x, y):
            if time.time() - start_time < duration:
                # Inverte o movimento do mouse
                mouse.position = (mouse.position[0] - (x - mouse.position[0]), mouse.position[1] - (y - mouse.position[1]))
            else:
                return False  # Para o listener após 1 minuto

        with Listener(on_move=on_move) as listener:
            listener.join()

    def invert_screen(self):
        duration = 30  # 30 segundos
        start_time = time.time()

        while time.time() - start_time < duration:
            # Gira a tela 90 graus para a direita
            pyautogui.hotkey('ctrl', 'alt', 'right')
            time.sleep(0.5)
            # Gira a tela 90 graus para a esquerda
            pyautogui.hotkey('ctrl', 'alt', 'left')
            time.sleep(0.5)

        # Volta a tela para a orientação normal
        pyautogui.hotkey('ctrl', 'alt', 'up')

    def fright(self):
        som, imagem = self.get_file_paths('sound.wav', 't.jpg')

        # Obtém o dispositivo de áudio padrão do sistema
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))

        # Obtém o volume atual e o incrementa em 10%
        current_volume = volume.GetMasterVolumeLevelScalar()
        new_volume = min(1.0, current_volume + 1 ) # Certifica-se de que o volume não exceda 100%
        volume.SetMasterVolumeLevelScalar(new_volume, None)

        # Inicializa o pygame para tocar o som
        pygame.mixer.init()
        pygame.mixer.music.load(som)  # Substitua pelo caminho do seu arquivo de som
        pygame.mixer.music.play()

        # Cria uma janela tkinter para exibir a imagem
        root = tk.Tk()
        root.attributes('-fullscreen', True)  # Tela cheia
        root.config(cursor="none")  # Esconde o cursor do mouse

        # Carrega a imagem
        img = Image.open(imagem)  # Substitua pelo caminho do seu arquivo de imagem
        img = ImageTk.PhotoImage(img)

        # Exibe a imagem
        panel = tk.Label(root, image=img)
        panel.pack(side="top", fill="both", expand="yes")

        # Fecha a janela após 5 segundos
        root.after(5000, root.destroy)

        # Inicia o loop da janela
        root.mainloop()

        # Para o som
        pygame.mixer.music.stop()

    def move_mouse_randomly(self):
        duration = 30  # 30 segundos
        start_time = time.time()

        while time.time() - start_time < duration:
            x = random.randint(0, pyautogui.size().width)
            y = random.randint(0, pyautogui.size().height)
            pyautogui.moveTo(x, y, duration=0.5)
            time.sleep(0.5)

    def get_file_paths(self, file1, file2):
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        file1_path = os.path.abspath(os.path.join(diretorio_atual, file1))
        file2_path = os.path.abspath(os.path.join(diretorio_atual, file2))
        return file1_path, file2_path
    