from turn_combat import CombatPlayer
""" Create PyGameAIPlayer class here"""


class PyGameAIPlayer:
    def selectAction(self, state):
        if str(state.current_city) == "0":
            return ord("1")  # Not a safe operation for >10 cities
        if str(state.current_city) == "1":
            return ord("2")  # Not a safe operation for >10 cities
        if str(state.current_city) == "2":
            return ord("3")  # Not a safe operation for >10 cities
        if str(state.current_city) == "3":
            return ord("4")  # Not a safe operation for >10 cities
        if str(state.current_city) == "4":
            return ord("5")  # Not a safe operation for >10 cities
        if str(state.current_city) == "5":
            return ord("6")  # Not a safe operation for >10 cities
        if str(state.current_city) == "6":
            return ord("7")  # Not a safe operation for >10 cities
        if str(state.current_city) == "7":
            return ord("8")  # Not a safe operation for >10 cities
        if str(state.current_city) == "8":
            return ord("9")  # Not a safe operation for >10 cities
        


""" Create PyGameAICombatPlayer class here"""


class PyGameAICombatPlayer(CombatPlayer):
    def __init__(self, name):
        super().__init__(name)
        
    def weapon_selecting_strategy(self):
        while True:
            self.weapon = 1
            return self.weapon
    


# class PyGameHumanCombatPlayer(CombatPlayer):
#     def __init__(self, name):
#         super().__init__(name)

#     def weapon_selecting_strategy(self):
#         while True:
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     pygame.quit()
#                 if event.type == pygame.KEYDOWN:
#                     if event.key in [ord("s"), ord("a"), ord("f")]:
#                         choice = {ord("s"): 1, ord("a"): 2, ord("f"): 3}[event.key]
#                         self.weapon = choice - 1
#                         return self.weapon