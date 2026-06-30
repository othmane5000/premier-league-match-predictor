"""
Launcher desktop pour Football Match Predictor.
Lance Streamlit en arrière-plan et ouvre l'app dans une fenêtre native (pywebview),
comme une vraie application desktop — sans barre d'adresse navigateur.
"""
import threading
import time
import socket
import sys
import os

import webview
from streamlit.web import cli as stcli


def get_free_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def resource_path(relative_path):
    """Trouve le bon chemin que ce soit en dev ou packagé par PyInstaller."""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def run_streamlit(port):
    app_path = resource_path(os.path.join("src", "app.py"))
    sys.argv = [
        "streamlit", "run", app_path,
        "--server.port", str(port),
        "--server.headless", "true",
        "--global.developmentMode", "false",
        "--server.enableCORS", "false",
        "--browser.gatherUsageStats", "false",
    ]
    stcli.main()


if __name__ == "__main__":
    port = get_free_port()

    # Lance Streamlit dans un thread en arrière-plan
    t = threading.Thread(target=run_streamlit, args=(port,), daemon=True)
    t.start()

    # Attendre que le serveur soit prêt
    time.sleep(3)

    # Ouvre l'app dans une vraie fenêtre desktop (sans barre d'adresse)
    webview.create_window(
        "Football Match Predictor",
        f"http://localhost:{port}",
        width=1280,
        height=860,
        min_size=(900, 600),
    )
    webview.start()
