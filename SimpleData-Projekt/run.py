import os
from SimpleData import app 

if __name__ == '__main__':#ustawiamy pod jak¹ nazw¹ mo¿e funkcjonowaæ nasza aplikacja w projekcie
    HOST = os.environ.get('SERVER_HOST', 'localhost')#ustawienia serverna na loklanyhost

    app.debug = True#linia któr¹ trzeba dodaæ aby zmiany w aplikacji odœiwrza³y siê po prze³adowaniu strony bez koniecznoœci prze³adowwywania serwera
    
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555

    app.run(HOST, PORT)
