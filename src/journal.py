import pygame

game_font = pygame.font.SysFont("Comic Sans MS", 30)

def draw_journal_on_window(journal_surface, screen, player): 

    screen.blit(journal_surface, (0, 0))
    money_surface = game_font.render("Player Money: "+str(round(player.money)), True, (220, 0, 0))
    turn_surface = game_font.render("Turn Number: "+str(player.turn_no), True, (220, 0, 0))
    instruction_journal_display = pygame.font.SysFont("Comic Sans MS", 15).render("close journal: c", True, (250, 0, 0))
    screen.blit(money_surface, (100, 250))
    screen.blit(turn_surface, (100, 300))
    screen.blit(instruction_journal_display, (100, 350))
    pygame.display.update()