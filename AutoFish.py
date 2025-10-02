import cv2
import easyocr
import pyautogui
import numpy
import time
from rich import print
import os
import keyboard

# ------------------------------------------------------------

# Limpa o terminal e exibe a mensagem de início
os.system('cls' if os.name == 'nt' else 'clear')
print("[bold deep_sky_blue1]Iniciando a Auto-Pesca...[/bold deep_sky_blue1]")
print("[yellow]Pressione 'i' a qualquer momento para parar.[/yellow]")
time.sleep(2)  # Pausa para o usuário se preparar

# --- CONFIGURAÇÕES ---
magicPhrase = "Fishing Bobber"
# Formato (esquerda, topo, LARGURA, ALTURA)
# Calcule a largura e altura corretas para a sua tela e resolução.
screenRegion = (1400, 700, 500, 300)
catchCount = 0

# gpu=False para maior compatibilidade. Mude para True apenas se tiver certeza.
print("[grey58]Carregando modelo de reconhecimento de texto (EasyOCR)...[/grey58]")
reader = easyocr.Reader(['en'], gpu=False)
print("[bold green]Modelo carregado. Pesca iniciada![/bold green]")
# ------------------------------------------------------------

pyautogui.click(button="right")  # Joga a primeira isca

while True:
    # Verifica se a tecla 'i' foi pressionada para parar o script
    if keyboard.is_pressed('i'):
        print("\n[bold red]Script interrompido pelo usuário.[/bold red]")
        break

    # Tira um print da região especificada
    screenCapture = pyautogui.screenshot(region=screenRegion)
    # Converte a imagem para o formato que o OpenCV/EasyOCR usa
    ocrImage = cv2.cvtColor(numpy.array(screenCapture), cv2.COLOR_RGB2BGR)

    # Lê o texto na imagem
    results = reader.readtext(ocrImage)

    phraseFound = False
    for result in results:
        text = result[1]
        if magicPhrase.lower() in text.lower():
            phraseFound = True
            break  # Para de procurar assim que encontra a frase

    if phraseFound:
        catchCount += 1
        print(f"[grey89]Peixe fisgado! Total: [bold cyan]{catchCount}[/bold cyan]", end="\r")

        # 1. Puxa a linha
        pyautogui.click(button="right")
        # Pausa curta para o jogo processar a captura
        time.sleep(0.5)
        # 2. Joga a linha novamente
        pyautogui.click(button="right")

        # Pausa maior para evitar verificar a tela logo após jogar a isca
        time.sleep(1.5)

    time.sleep(0.1)  # Pausa curta para não sobrecarregar o processador

# ------------------------------------------------------------
print("\nFinalizando o script.")
reader.close()