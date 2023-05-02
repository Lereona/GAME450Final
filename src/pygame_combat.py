import pygame
from pathlib import Path
import random

from sprite import Sprite
from turn_combat import CombatPlayer, Combat
from pygame_ai_player import PyGameAICombatPlayer
from pygame_human_player import PyGameHumanCombatPlayer


AI_SPRITE_PATH = Path("assets/ai.png")

pygame.font.init()
game_font = pygame.font.SysFont("Comic Sans MS", 15)


class PyGameComputerCombatPlayer(CombatPlayer):
    def __init__(self, name):
        super().__init__(name)

    def weapon_selecting_strategy(self):
        if 30 < self.health <= 50:
            self.weapon = 2
        elif self.health <= 30:
            self.weapon = 1
        else:
            self.weapon = 0
        return self.weapon


def run_turn(currentGame, player, opponent):
    players = [player, opponent]
    states = list(reversed([(player.health, player.weapon) for player in players]))
    for current_player, state in zip(players, states):
        current_player.selectAction(state)

    currentGame.newRound()
    currentGame.takeTurn(player, opponent)
    print("%s's health = %d" % (player.name, player.health))
    print("%s's health = %d" % (opponent.name, opponent.health))
    reward = currentGame.checkWin(player, opponent)
    return reward

def random_bot_taunt(message):
    return (pygame.font.SysFont("Comic Sans MS", 15).render("Thief: " + message, True, (220, 0, 0)))

def random_player_taunt(message):
    return (pygame.font.SysFont("Comic Sans MS", 15).render("You: " + message, True, (220, 0, 0)))


def draw_combat_on_window(combat_surface, screen, player_sprite, opponent_sprite, player, opponent, bot_taunt_list, player_taunt_list):
    screen.blit(combat_surface, (0, 0))
    player_sprite.draw_sprite(screen)
    opponent_sprite.draw_sprite(screen)
    text_surface = game_font.render("Choose s-Sword a-Arrow f-Fire!", True, (220, 0, 0))
    screen.blit(text_surface, (50, 50))
    screen.blit(random_bot_taunt(random.choice(bot_taunt_list)), (50, 500))
    screen.blit(random_player_taunt(random.choice(player_taunt_list)), (50, 550))
    player_health = pygame.font.SysFont("Comic Sans MS", 25).render("Your HP: "+str(player.health), True, (220, 0, 0))
    bot_health = pygame.font.SysFont("Comic Sans MS", 25).render("Thief HP: "+str(opponent.health), True, (220, 0, 0))
    screen.blit(player_health, (50, 300))
    screen.blit(bot_health, (50, 350))
    pygame.display.update()


def run_pygame_combat(combat_surface, screen, player_sprite, bot_taunt_list, player_taunt_list):
    currentGame = Combat()
    player = PyGameHumanCombatPlayer("Legolas")
    """ Add a line below that will reset the player object
    to an instance of the PyGameAICombatPlayer class"""
    #player = PyGameAICombatPlayer("Joe")

    opponent = PyGameComputerCombatPlayer("Computer")
    opponent_sprite = Sprite(
        AI_SPRITE_PATH, (player_sprite.sprite_pos[0] - 100, player_sprite.sprite_pos[1])
    )

    counter = 0
    # Main Game Loop
    while not currentGame.gameOver:
        draw_combat_on_window(combat_surface, screen, player_sprite, opponent_sprite, player, opponent, bot_taunt_list, player_taunt_list)
        result = run_turn(currentGame, player, opponent)
    return result

        
