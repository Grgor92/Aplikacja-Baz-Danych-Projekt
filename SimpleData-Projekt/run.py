import os
from SimpleData import app 

if __name__ == '__main__':
    HOST = os.environ.get('SERVER_HOST', 'localhost')

    app.debug = True
    
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555

    app.run(HOST, PORT)
