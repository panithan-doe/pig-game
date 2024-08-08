import socket
from player import Player
from diceGame import DiceGame
import random


def start_server(host='127.0.0.1', port=8080):
    

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Server listening on {host}:{port}")
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")

            diceGame = DiceGame()
            while True:
                data = conn.recv(1024)
                if not data:
                    break

                message = data.decode().strip().lower()
                print(f"Received: {message}")
                
                if (message == "dice") and (diceGame.isPlaying == False):
                    handlePlayer(diceGame, conn)                
                    diceGame.start()    # set isPlaying = True
                    response = f"Game is started!\n[{diceGame.players[0].name.upper()}] turn! ('roll'🎲 or 'hold'⬇️)"
                    conn.sendall(response.encode())
                                  
            
                elif diceGame.isPlaying:
                    currentPlayer = diceGame.players[diceGame.turn]
                    response = "Enter your action('roll'🎲 or 'hold'⬇️)"                                                
                    
                    if message == "roll":
                        dieValue = random.randint(1, 6)
                        print(f"[{currentPlayer.name.upper()}] rolled, die value = {dieValue}")
                        # random value = 1
                        if dieValue == 1:
                            response = f"Die value is 1💥\n[{diceGame.players[1 - diceGame.turn].name.upper()}] turn! ('roll'🎲 or 'hold'⬇️)"
                            currentPlayer.reset_temp_score()
                            diceGame.swapTurn()
                            
                        else:
                            currentPlayer.increaseTempScore(dieValue)
                            response = f">> {dieValue}\nTemp: {currentPlayer.temp_score} ('roll'🎲 again or 'hold'⬇️)"
                        
                        conn.sendall(response.encode())
                    
                    elif message == "hold":
                        currentPlayer.hold()
                        response = f"Hold!\n{currentPlayer}\n[{diceGame.players[1 - diceGame.turn].name.upper()}] turn! ('roll'🎲 or 'hold'⬇️)"
                        
                        if currentPlayer.total_score >= 60:
                            response = f"{currentPlayer.name.upper()} wins! Play again?('y')"
                            conn.sendall(response.encode())
                            
                            data = conn.recv(1024)
                            print(f"Received: {data.decode()}")
                            if data.decode().strip().lower() == 'y':
                                print("Game restart.")
                                diceGame.reset_game()
                                response = "New game started! Type 'dice' to begin."
                            else:
                                response = "Thank you for playing! Goodbye!"
                                conn.sendall(response.encode())
                                break

                            conn.sendall(response.encode())
                            
                            continue

                            # break

                        diceGame.swapTurn()
                        conn.sendall(response.encode())

                    else:
                        response = "Wrong command, please type 'roll' or 'hold'."
                        conn.sendall(response.encode())

                else:
                    response = "Wrong command, please type 'dice' to start."
                    
                    conn.sendall(response.encode())


def handlePlayer(diceGame, conn):
    conn.sendall("Enter player 1 name: ".encode())
    player1_name = conn.recv(1024).decode().strip()
    print(f"Received player(1) name: {player1_name}")
    print(f"Waiting for player(2)...")

    conn.sendall("Enter player 2 name: ".encode())
    player2_name = conn.recv(1024).decode().strip()
    print(f"Received player(2) name: {player2_name}")

    # add players
    diceGame.players[0] = Player(player1_name)
    diceGame.players[1] = Player(player2_name)

    print(f"Both player is ready!")

if __name__ == "__main__":
    start_server()
