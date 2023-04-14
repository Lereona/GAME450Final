''' 
Lab 12: Beginnings of Reinforcement Learning
We will modularize the code in pygrame_combat.py from lab 11 together.

Then it's your turn!
Create a function called run_episode that takes in two players
and runs a single episode of combat between them. 
As per RL conventions, the function should return a list of tuples
of the form (observation/state, action, reward) for each turn in the episode.
Note that observation/state is a tuple of the form (player1_health, player2_health).
Action is simply the weapon selected by the player.
Reward is the reward for the player for that turn.
'''

import sys
from pathlib import Path
sys.path.append(str((Path(__file__) / ".." / "..").resolve().absolute()))
from pygame_combat import run_turn

# # #testing
from turn_combat import Combat
# from lab11.pygame_ai_player import PyGameAICombatPlayer
# from lab11.pygame_combat import PyGameComputerCombatPlayer



def run_episode(player, opponent):
    currentGame = Combat()
    episode = []
    # episode += [((player.health, opponent.health), player.weapon, currentGame.checkWin(player, opponent))]
    while (currentGame.gameOver == False):
        if(opponent.health <= 0 or player.health <= 0):   
            break

        playerHealth = player.health
        opponentHealth = opponent.health
        reward = run_turn(currentGame,player,opponent)
        
        episode.append(((playerHealth, opponentHealth),player.action, reward))
    return episode

# #testing
# newgame = Combat()
# player = PyGameAICombatPlayer("you")
# #player.health = 50
# opponent = PyGameComputerCombatPlayer("bot")
# opponent.health = 50

# new_episode = run_episode(player, opponent)
    
# print(new_episode)