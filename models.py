class Jogo:
  def __init__(self, nome, categoria, console, id = None):
    self.id = id
    self.nome = nome
    self.categoria = categoria
    self.console = console

class Usuario:
  def __init__(self, nome, nickname, senha):
    self.nome = nome
    self.nickname = nickname
    self.senha = senha