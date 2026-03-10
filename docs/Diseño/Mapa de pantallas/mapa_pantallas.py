from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from graphviz import Digraph
import time

# Configurar Chromedriver
service = Service("/usr/bin/chromedriver")  # ajusta si tu chromedriver está en otra ruta
options = webdriver.ChromeOptions()
options.add_argument("--window-size=1280,800")
# options.add_argument("--headless")  # comenta si quieres ver la ventana

driver = webdriver.Chrome(service=service, options=options)

# --- LOGIN ADMIN ---
driver.get("http://127.0.0.1:5000/login")
time.sleep(2)

driver.find_element(By.NAME, "email").send_keys("admin@cimacritics.com")
driver.find_element(By.NAME, "password").send_keys("admin123")
driver.find_element(By.NAME, "submit").click()

time.sleep(2)
print("Login admin realizado")

# Diccionario de pantallas y sus URLs
urls = {
    "index": "http://127.0.0.1:5000/",
    "comics": "http://127.0.0.1:5000/comics",
    "comic_detail": "http://127.0.0.1:5000/comics/1",   # ejemplo con comic_id=1
    "perfil": "http://127.0.0.1:5000/perfil/1",          # ejemplo con user_id=1
    "admin_dashboard": "http://127.0.0.1:5000/admin",
    "add_comic": "http://127.0.0.1:5000/admin/comic/add",
    "logout": "http://127.0.0.1:5000/logout",
    "register": "http://127.0.0.1:5000/register"
}

# Tomar capturas de cada pantalla
for name, url in urls.items():
    try:
        driver.get(url)
        time.sleep(2)
        driver.save_screenshot(f"{name}.png")
        print(f"Captura guardada: {name}.png")
    except Exception as e:
        print(f"No se pudo capturar {name}: {e}")

driver.quit()

# Crear grafo con imágenes incrustadas
dot = Digraph(comment="Mapa de pantallas CimaCritics")
dot.attr(rankdir="LR", size="8")

for name in urls.keys():
    dot.node(name, label=name, image=f"{name}.png", shape="rect")

# Conexiones principales
dot.edge("index", "comics")
dot.edge("comics", "comic_detail")
dot.edge("comic_detail", "perfil")
dot.edge("index", "admin_dashboard")
dot.edge("admin_dashboard", "add_comic")
dot.edge("index", "register")
dot.edge("index", "logout")

# Exportar a PNG y SVG
dot.render("mapa_pantallas", format="png")
dot.render("mapa_pantallas", format="svg")
print("Mapa de pantallas generado en mapa_pantallas.png y mapa_pantallas.svg")
