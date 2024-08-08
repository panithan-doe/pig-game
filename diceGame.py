class DiceGame:
  def __init__(self):
    self.players = [None, None]
    self.turn = 0
    self.isPlaying = False

  def swapTurn(self):
    if self.turn == 0:
      self.turn = 1
    elif self.turn == 1:
      self.turn = 0

  def start(self) -> str:
    if None not in self.players:
      self.isPlaying = True
      print("Game is playing...")
    else:
      return "Both players must be added before starting the game."

  def reset_game(self):
    self.isPlaying = False
    self.players = [None, None]
    self.turn = 0
