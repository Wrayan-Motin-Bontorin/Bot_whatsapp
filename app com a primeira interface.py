import tkinter as tk
from tkinter import filedialog
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd
import urllib
import os

class WhatsappBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("WhatsApp Bot")
        
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=20, pady=20)
        
        self.message_label = tk.Label(self.frame, text="Digite a mensagem:", )
        self.message_label.pack()
        self.message_entry = tk.Entry(self.frame, width=50)
        self.message_entry.pack()

        self.browse_db_button = tk.Button(self.frame, text="Selecionar Arquivo de DB", command=self.select_db_file)
        self.browse_db_button.pack()
        
        self.browse_button = tk.Button(self.frame, text="Selecionar Arquivos", command=self.select_files)
        self.browse_button.pack()

        self.start_button = tk.Button(self.frame, text="Iniciar Envio", command=self.start_sending)
        self.start_button.pack()
        
        self.selected_files = []

        self.driver = None

    def select_files(self):
        self.selected_files = filedialog.askopenfilenames()
        
    def select_db_file(self):
        self.selected_db_file = filedialog.askopenfilename()

    def start_sending(self):
        message = self.message_entry.get()
        self.configura_navegador()
        self.lista(message)

    def configura_navegador(self):
        chrome_options = Options()
        arguments = ['--lang=pt-BR', '--window-size=800,900', '--disable-notifications', '--incognito', 'eager']
        for argument in arguments:
            chrome_options.add_argument(argument)
        chrome_options.add_experimental_option('prefs', {
            'download.default_directory': 'C:\\Users\\wramo\\OneDrive\\Área de Trabalho\\mod\\downloads',
            'download.directory_upgrade': True,
            'download.prompt_for_download': False,
            'profile.default_content_setting_values.notifications': 2,
            'profile.default_content_setting_values.automatic_downloads': 1,
        })
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

    def lista(self, message):
        self.driver.get("https://web.whatsapp.com/")
        while len(self.driver.find_elements(By.ID, 'side')) < 1:
            sleep(1)
        sleep(2)
        self.ler_telefones(message)

    def ler_telefones(self, message):
        db = pd.read_excel(self.selected_db_file)
        for linha in db.index:
            telefone = db.loc[linha, 'telefone']
            message = message

            link = f'http://web.whatsapp.com/send?phone={telefone}'
            self.driver.get(link)
            while len(self.driver.find_elements(By.XPATH, '//*[@id="main"]/header/div[2]')) < 1:
                sleep(1)
            sleep(2)
            self.driver.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div[2]/div[1]').send_keys(message) # envia o texto a mensagem
            sleep(1)
            self.driver.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button').click() # envia o texto a mensagem
            

            for file_path in self.selected_files:
                self.driver.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div/div/div/div/span').click() # clica no botao de anexo
                sleep(.5)
                self.driver.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div/div/span/div/ul/div/div[2]/li/div/input').send_keys(file_path) # passa direto no imput o caminho da imagem
                sleep(1)
                self.driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/div[2]/span/div/span/div/div/div[2]/div/div[2]/div[2]/div/div').click() # Envia a imagem
                sleep(2)
#  
if __name__ == "__main__":
    root = tk.Tk()
    app = WhatsappBotGUI(root)
    root.mainloop()
