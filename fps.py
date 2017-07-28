
# Let different things handle different players (decouple it).

class Multiplayer:
    # This class can act on all players based on what's received over the network.


class Local:
    # This class can act on the 



# Actually I'm not seein that working... there maybe should be one class that handles all the players' movement, etc. Instead of one that that handles other player's movement and one that handles the local player's movement?


# Yes it should be different since the local user input should happen instantly whereas what is received over the network needs to happen when it's received so a separate class should tell those players what to do, I think.

# Multiplayer -> game.ships.add...
# holds a list of players based on their id


class Player:
    def move: pass
    def shoot: pass


#https://gamedevelopment.tutsplus.com/tutorials/building-a-peer-to-peer-multiplayer-networked-game--gamedev-10074
#https://stackoverflow.com/questions/23267305/python-sockets-peer-to-peer


# P2P

#Create two sockets per peer
#Get an ip from the peer

import socket

def get_ip():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(("10.255.255.255", 1))
        ip = s.getsockname()[0]
    return ip

"""
Each peer runs the same code:
    Get lan ip
    Listen for client connections on port 1500
     - Accept connections on port 1501 over TCP
     - Run listening socket on a new thread preferably
    Client socket binds to other peers on port 1501
"""


server_port = 1500
client_port = 1501

#---
# Diff file tool.
# Ex.
# generate log: expected output
# for each new log: compare to correct log and check for differences
