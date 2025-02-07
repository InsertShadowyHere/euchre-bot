from Game import Game
from Players import *


"""
todo
add graphics
code bot
"""


# p1 = Player(input("What's your name?\n"))
p1 = Player("Raphael")
p2 = Bot("Tofurkey")
p3 = Bot("A-A-ron")
p4 = Bot("KFC")
t1 = Team("The Midgets", p1, p2)
t2 = Team("The Nerds", p3, p4)

game = Game(t1, t2)

game.run()
