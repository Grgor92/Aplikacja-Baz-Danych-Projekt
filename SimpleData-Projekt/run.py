import os
from SimpleData import app 

if __name__ == '__main__':#ustawiamy pod jak� nazw� mo�e funkcjonowa� nasza aplikacja w projekcie
    HOST = os.environ.get('SERVER_HOST', 'localhost')#ustawienia serverna na loklanyhost

    app.debug = True#linia kt�r� trzeba doda� aby zmiany w aplikacji od�iwrza�y si� po prze�adowaniu strony bez konieczno�ci prze�adowwywania serwera
    
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555

    app.run(HOST, PORT)
