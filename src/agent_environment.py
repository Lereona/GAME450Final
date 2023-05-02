import sys
import pygame
import random
from sprite import Sprite
from pygame_combat import run_pygame_combat
from pygame_human_player import PyGameHumanPlayer
from landscape import get_landscape, get_combat_bg, get_elevation, elevation_to_rgba
from pygame_ai_player import PyGameAIPlayer
from text_generation import player_taunt_pool, bot_taunt_pool

from pathlib import Path

sys.path.append(str((Path(__file__) / ".." / "..").resolve().absolute()))

from cities_n_routes import get_randomly_spread_cities, get_routes
from ga_cities import solution_to_cities, ga_func
from journal import draw_journal_on_window

pygame.font.init()
game_font = pygame.font.SysFont("Comic Sans MS", 15)


def load_image(image_path):
    image = pygame.image.load(image_path).convert_alpha()
    return image


def get_landscape_surface(size):
    elevation = get_elevation(size)
    landscape = elevation_to_rgba(elevation)
    #landscape = get_landscape(size)
    print("Created a landscape of size", landscape.shape)
    pygame_surface = pygame.surfarray.make_surface(landscape[:, :, :3])
    return pygame_surface, elevation

def get_combat_surface(size):
    pygame_surface = load_image("assets/forest.png")
    pygame_surface = pygame.transform.scale(pygame_surface, size)
    print("Loaded combat surface")
    return pygame_surface

#added journaling mechanism
def get_journal_surface(size):
    pygame_surface = load_image("assets/journal.png")
    pygame_surface = pygame.transform.scale(pygame_surface, size)    
    print("Loaded journal surface")
    return pygame_surface



def setup_window(width, height, caption):
    pygame.init()
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption(caption)
    return window


def displayCityNames(city_locations, city_names):
    for i, name in enumerate(city_names):
        text_surface = game_font.render(str(i) + " " + name, True, (0, 0, 150))
        screen.blit(text_surface, city_locations[i])


class State:
    def __init__(
        self,
        current_city,
        destination_city,
        travelling,
        encounter_event,
        cities,
        routes,
    ):
        self.current_city = current_city
        self.destination_city = destination_city
        self.travelling = travelling
        self.encounter_event = encounter_event
        self.cities = cities
        self.routes = routes


if __name__ == "__main__":
    size = width, height = 640, 640
    black = 1, 1, 1
    start_city = 0
    end_city = 9
    sprite_path = "assets/lego.png"
    sprite_speed = 1
    bot_taunt_list = bot_taunt_pool()
    player_taunt_list = player_taunt_pool()
    print("Loaded AI generated messages")
    screen = setup_window(width, height, "Lost Wanderer of Elysia")

    landscape_surface, elevation = get_landscape_surface(size)
    combat_surface = get_combat_surface(size)
    journal_surface = get_journal_surface(size)

    city_names = [
        "Morkomasto",
        "Morathrad",
        "Eregailin",
        "Corathrad",
        "Eregarta",
        "Numensari",
        "Rhunkadi",
        "Londathrad",
        "Baernlad",
        "Forthyr",
    ]

    #cities = get_randomly_spread_cities(size, len(city_names))
    n_cities = 10
    cities = ga_func(elevation, n_cities, size)

    
    routes = get_routes(cities)

    random.shuffle(routes)
    routes = routes[:20]

    player_sprite = Sprite(sprite_path, cities[start_city])

    player = PyGameHumanPlayer()

    """ Add a line below that will reset the player variable to 
    a new object of PyGameAIPlayer class."""
    #player = PyGameAIPlayer()

    state = State(
        current_city=start_city,
        destination_city=start_city,
        travelling=False,
        encounter_event=False,
        cities=cities,
        routes=routes,
    )

    while True:
        action = player.selectAction(state)
        #open/close journal
        if chr(action) == "j":
                if not state.travelling:
                    while not (chr(action) == "c"):
                        action = player.selectAction(state)
                        draw_journal_on_window(journal_surface, screen, player)
        if chr(action) =="c":
            print("")
        #select city
        elif 0 <= int(chr(action)) <= 9:
            in_route = False
            if int(chr(action)) != state.current_city and not state.travelling:
                #logic to check for valid route  
                for route in routes:
                    if ((route[0] == cities[state.current_city]).all() and (route[1] == cities[int(chr(action))]).all()) or \
                            ((route[1] == cities[state.current_city]).all() and (route[0] == cities[int(chr(action))]).all()):
                        in_route = True
                        break

            if in_route:
                if int(chr(action)) != state.current_city and not state.travelling:
                    start = cities[state.current_city]
                    state.destination_city = int(chr(action))
                    destination = cities[state.destination_city]
                    player_sprite.set_location(cities[state.current_city])
                    state.travelling = True
                    print(
                        "Travelling from", state.current_city, "to", state.destination_city
                    )
                    #traveling cost based on elevation height
                    player.money = player.money - abs(50*(elevation[cities[state.destination_city][0]][cities[state.destination_city][1]]))
                    player.turn_no +=1
                    #lose if no money
                    if player.money <= 0:
                        print("GAME OVER, ran out of money!")
                        print("Turns took: "+str(player.turn_no))
                        pygame.quit()
                        sys.exit()
                        break
                    #win if over $150
                    if player.money >= 150:
                        print("YOU WON! $150 REACHED")
                        print("Turns took: "+str(player.turn_no))
                        pygame.quit()
                        sys.exit()
                        break
            

        screen.fill(black)
        screen.blit(landscape_surface, (0, 0))
        #displays money
        stamina_display = pygame.font.SysFont("Comic Sans MS", 30).render("Money: $"+str(round(player.money)), True, (250, 0, 0))
        screen.blit(stamina_display, (100,500))
        #display instructions
        instruction_city_display = pygame.font.SysFont("Comic Sans MS", 15).render("choose city to travel: 1-9", True, (250, 0, 0))
        instruction_journal_display = pygame.font.SysFont("Comic Sans MS", 15).render("open journal: j", True, (250, 0, 0))
        screen.blit(instruction_city_display, (100,600))
        screen.blit(instruction_journal_display, (100,550))

        for city in cities:
            pygame.draw.circle(screen, (255, 0, 0), city, 5)

        for line in routes:
            pygame.draw.line(screen, (255, 0, 0), *line)

        displayCityNames(cities, city_names)
        if state.travelling:
            state.travelling = player_sprite.move_sprite(destination, sprite_speed)
            state.encounter_event = random.randint(0, 1000) < 2
            if not state.travelling:
                print('Arrived at', state.destination_city)

        if not state.travelling:
            encounter_event = False
            state.current_city = state.destination_city

        if state.encounter_event:
            player.turn_no +=1
            result = run_pygame_combat(combat_surface, screen, player_sprite, bot_taunt_list, player_taunt_list)
            #handles win or lose battle results
            if result == 1:
                player.money += 25
                print("Won battle, earned $25")
                print("Turn: "+str(player.turn_no))
                #win if over $150
                if player.money >= 150:
                    print("YOU WON! $150 REACHED")
                    print("Turns took: "+str(player.turn_no))
                    pygame.quit()
                    sys.exit()
                    break
            if result == -1:
                print("Game OVER, ran out of HP!")
                print("Turns took: "+str(player.turn_no))
                pygame.quit()
                sys.exit()
                break
            state.encounter_event = False
        else:
            player_sprite.draw_sprite(screen)
        pygame.display.update()
        # if state.current_city == end_city:
        #     print('You have reached the end of the game!')
        #     break
