import game

# LEVELMANAGER.PY TRACKS THE LEVEL THAT THE PLAYER IS ON. CURRENTLY JUST CHANGES WITH TIME. 

class LevelManager():
    def __init__(self):

        self.level = 1
        self.timer = 0


    def update(self, dt, game):
        open_shop = False
        self.timer += dt

        if self.timer > 60:
            open_shop = True
            self.level += 1
            self.timer = 0
            game.clear_entities()

        print(self.level)
        
        return self.level, open_shop