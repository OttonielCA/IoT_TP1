import paho.mqtt.client as mqtt
import time

# Ceci est le script pour executer le commandeur dans le terminal

broker = "test.mosquitto.org"  # adresse du rboker mqtt
port = 1883  # Port MQTT par défaut
qos = 2  # Niveau de QoS

topic_pieton = "mode/pieton"
topic_panne = "mode/panne"
topic_urgence = "mode/urgence"
def publish_pieton_command(client):
    client.publish(topic_pieton, "pieton_on")
    print("Commande 'pieton_on' envoyee.")

def publish_panne_command(client, command):
    client.publish(topic_panne, command)
    print(f"Commande '{command}' envoyee.")

def publish_urgence_command(client, command):
    client.publish(topic_urgence, command)
    print(f"Commande '{command}' envoyee.")

# Creer une instance du client
client = mqtt.Client()

# Se connecter au broker
client.connect(broker, port, 60)

# Publier un message
client.loop_start()

try:
    while True:
        user_input = int(input("mode pieton: 1\nmode panne: 2\nmode urgence: 3\nQuel mode voulez vous executer: "))
        if user_input == 1:
            publish_pieton_command(client)
        elif user_input == 2:
            panne = "panne_on"
            publish_panne_command(client, panne)
            while panne == "panne_on":
                panne_input = int(input("Entrez '1' pour sortir du mode panne ou '2' pour passer en mode urgence: "))
                if panne_input == 1:
                    panne = "panne_off"
                    publish_panne_command(client, panne)
                elif panne_input == 2:
                    urgence_input = int(input("Entrez la direction a changer vers le vert (entrez 1 pour 'direction 1' ou 2 pour 'direction 2'): "))
                    if urgence_input == 1:
                        urgence = "urgence_direction1"
                        publish_urgence_command(client, urgence)
                    elif urgence_input == 2:
                        urgence = "urgence_direction2"
                        publish_urgence_command(client, urgence)
                    else:
                        print("Mauvaise entree, reesaayer")
                        time.sleep(1)
                else:
                    print("Mauvaise entree, reesaayer")
                    time.sleep(1)
        elif user_input == 3:
            urgence = ""
            while urgence == "":
                urgence_input = int(input("Entrez la direction a changer vers le vert (entrez 1 pour 'direction 1' ou 2 pour 'direction 2'): "))
                if urgence_input == 1:
                    urgence = "urgence_direction1"
                    publish_urgence_command(client, urgence)
                elif urgence_input == 2:
                    urgence = "urgence_direction2"
                    publish_urgence_command(client, urgence)
                else:
                    print("Mauvaise entree, reesaayer")
                    time.sleep(1)
        else:
            print("Mauvaise entree, reesaayer")
            time.sleep(1)
except KeyboardInterrupt:
    print("Exiting...")
finally:
    client.loop_stop()
    client.disconnect()
