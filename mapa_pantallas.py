from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from graphviz import Digraph
import time

# Configurar Chromedriver
service = Service("/usr/bin/chromedriver")  # ajusta si está en otra ruta
options = webdriver.ChromeOptions()
# Quita el comentario si quieres ver la ventana
# options.add_argument("--headless")
options.add_argument("--window-size=1280,800")

driver = webdriver.Chrome(service=service, options=options)

# Diccionario de pantallas y sus URLs
urls = {
    "index": "http://127.0.0.1:5000/",
    "comics": "http://127.0.0.1:5000/comics",
    "login": "http://127.0.0.1:5000/login",
    "register": "http://127.0.0.1:5000/register",
    "perfil": "http://127.0.0.1:5000/perfil/1",
    "admin_dashboard": "http://127.0.0.1:5000/admin"
}

# Tomar capturas de cada pantalla
for name, url in urls.items():
    driver.get(url)
    time.sleep(2)
    driver.save_screenshot(f"{name}.png")
    print(f"Captura guardada: {name}.png")

driver.quit()

# Crear grafo con imágenes incrustadas
dot = Digraph(comment="Mapa de pantallas CimaCritics")
dot.attr(rankdir="LR", size="8")

for name in urls.keys():
    dot.node(name, label=name, image=f"{name}.png", shape="rect")

# Conexiones principales
dot.edge("index", "comics")
dot.edge("index", "login")
dot.edge("login", "register")
dot.edge("index", "perfil")
dot.edge("index", "admin_dashboard")

# Exportar a PNG y SVG
dot.render("mapa_pantallas", format="png")
dot.render("mapa_pantallas", format="svg")
print("Mapa de pantallas generado en mapa_pantallas.png y mapa_pantallas.svg")
