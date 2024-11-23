import time
from pynput.mouse import Controller, Listener
import pyautogui
from PIL import Image
from PIL import ImageTk
import tkinter as tk
import pygame
import subprocess
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import random
import os
import webbrowser

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
            case 'turn off monitor':
                self.turn_off_monitor()
            case 'open multiple browsers':
                self.open_multiple_browsers()

    def invert_mouse(self):
        mouse = Controller()

        start_time = time.time()
        duration = 60  # 1 minuto

        def on_move(x, y):
            if time.time() - start_time < duration:
                mouse.position = (mouse.position[0] - (x - mouse.position[0]), mouse.position[1] - (y - mouse.position[1]))
            else:
                return False  

        with Listener(on_move=on_move) as listener:
            listener.join()

    def invert_screen(self):
        duration = 30  # 30 segundos
        start_time = time.time()

        while time.time() - start_time < duration:
            pyautogui.hotkey('ctrl', 'alt', 'right')
            time.sleep(0.5)
            pyautogui.hotkey('ctrl', 'alt', 'left')
            time.sleep(0.5)

        pyautogui.hotkey('ctrl', 'alt', 'up')

    def fright(self):
        som, imagem = self.get_file_paths('sound.wav', 't.jpg')

        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))

        current_volume = volume.GetMasterVolumeLevelScalar()
        new_volume = min(1.0, current_volume + 1 )
        volume.SetMasterVolumeLevelScalar(new_volume, None)

        pygame.mixer.init()
        pygame.mixer.music.load(som)  
        pygame.mixer.music.play()

        root = tk.Tk()
        root.attributes('-fullscreen', True)  
        root.config(cursor="none")

        img = Image.open(imagem)  
        img = ImageTk.PhotoImage(img)

        panel = tk.Label(root, image=img)
        panel.pack(side="top", fill="both", expand="yes")

        root.after(5000, root.destroy)

        root.mainloop()

        pygame.mixer.music.stop()

    def move_mouse_randomly(self):
        duration = 30 
        start_time = time.time()

        while time.time() - start_time < duration:
            x = random.randint(0, pyautogui.size().width)
            y = random.randint(0, pyautogui.size().height)
            pyautogui.moveTo(x, y, duration=0.5)
            time.sleep(0.5)

    def turn_off_monitor(self):
        subprocess.call(["nircmd.exe", "monitor", "off"])
        time.sleep(60) 
        subprocess.call(["nircmd.exe", "monitor", "on"])

    def open_multiple_browsers(self):
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley"  
        for _ in range(20): 
            webbrowser.open(url)

    def get_file_paths(self, file1, file2):
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        file1_path = os.path.abspath(os.path.join(diretorio_atual, file1))
        file2_path = os.path.abspath(os.path.join(diretorio_atual, file2))
        return file1_path, file2_path
    
