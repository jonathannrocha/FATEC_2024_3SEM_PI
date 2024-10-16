from mongoengine import connect

# Temporario
def connectMongoDB():
    connect('userPerfil', host='localhost', port=27017)
    print("Conectado ao MongoDB")
