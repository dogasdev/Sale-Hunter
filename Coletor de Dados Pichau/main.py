import pandas as pd 
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--lang=pt")

service = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=service, options=chrome_options)
navegador.get("https://www.pichau.com.br/promocao/cliente")
time.sleep(5)

def scroll_page():
    antiga_altura = navegador.execute_script("return document.body.scrollHeight")
    while True:
        navegador.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        nova_altura = navegador.execute_script("return document.body.scrollHeight")
        if nova_altura == antiga_altura:
            break
        antiga_altura = nova_altura

scroll_page()

cards_produto = navegador.find_elements(By.CSS_SELECTOR, "h2.MuiTypography-root.MuiTypography-h6")

produtos = []

for card in cards_produto:
    try:
        nome = card.text.strip()
    except:
        nome = None
    
    try: 
        preco_original = card.find_element(By.XPATH, "./ancestor::div[contains(@class,'MuiCardContent-root')]//span[contains(@class,'strikeThrough')]").text.strip()
    except:
        preco_original = None

    try:
        preco_final = card.find_element(By.XPATH, "./ancestor::div[contains(@class,'MuiCardContent-root')]//div[contains(@class,'price_vista')]").text.strip()
    except:
        preco_final = None
    
    #print(f"{nome} | De: {preco_original} | Por: {preco_final}")  # debug

    produtos.append({
        "Nome": nome,
        "Preço Original": preco_original,
        "Preço Final": preco_final
    })

navegador.quit()
df = pd.DataFrame(produtos)
df.to_csv("pichau_promocoes.csv")
print(df)