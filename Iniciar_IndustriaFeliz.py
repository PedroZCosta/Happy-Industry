import subprocess
import webbrowser

def start_application():

    # inicia o bat do servidor
    subprocess.Popen(["IndustriaFeliz.bat"], shell=True)

    # abre o browser no endereço do servidor
    webbrowser.open("http://127.0.0.1:5000/")

if __name__ == "__main__":
    start_application()


#para gerar o arquivo pyinstaller --onefile start_app.py