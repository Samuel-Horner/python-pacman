import time
import kb_input

class Pos:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        return Pos(self.x + other.x, self.y + other.y)
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __sub__(self, other):
        return Pos(self.x - other.x, self.y - other.y)

    def calc_distance(self, other):
        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2 

movement_array = [Pos(0,-1), Pos(1,0), Pos(0,1), Pos(-1,0)]


class Entity:
    def __init__(self, x: int, y: int):
        self.pos = Pos(x, y)

    def get_sprite(): return None

class Ghost(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.dir = 1
        self.last_pos = self.pos
        self.scared = False
        self.cd = 0

    def move(self): pass

class Blinky(Ghost): # Red
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.home_pos = Pos(0,0)

    def get_sprite(self):
        if self.scared: return "\x1b[1;37m\u15E3\x1b[0m"
        return "\x1b[1;31m\u15E3\x1b[0m"
    
    def move(self, game_board, goal_pos):
        if self.cd > 0: 
            self.cd -= 1
            return
        if self.scared: goal_pos = self.home_pos
        min_dist = -1
        min_new_pos = self.pos
        for i in movement_array:
            new_pos = self.pos + i
            if game_board[new_pos.y][new_pos.x] == 1 or new_pos == self.last_pos: continue
            dist = new_pos.calc_distance(goal_pos)
            if min_dist == -1 or dist < min_dist:
                min_dist = dist
                min_new_pos = new_pos
        self.last_pos = self.pos
        self.pos = min_new_pos

class Pinky(Ghost): # Pink
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.home_pos = Pos(18,0)
    
    def get_sprite(self):
        if self.scared: return "\x1b[1;37m\u15E3\x1b[0m"
        return "\x1b[1;35m\u15E3\x1b[0m"
    
    def move(self, game_board, goal_pos):
        if self.cd > 0: 
            self.cd -= 1
            return
        if self.scared: goal_pos = self.home_pos
        min_dist = -1
        min_new_pos = self.pos
        for i in movement_array:
            new_pos = self.pos + i
            if game_board[new_pos.y][new_pos.x] == 1 or new_pos == self.last_pos: continue
            dist = new_pos.calc_distance(goal_pos)
            if min_dist == -1 or dist < min_dist:
                min_dist = dist
                min_new_pos = new_pos
        self.last_pos = self.pos
        self.pos = min_new_pos
    
class Inky(Ghost): # Cyan
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.home_pos = Pos(0,10)

    def get_sprite(self):
        if self.scared: return "\x1b[1;37m\u15E3\x1b[0m"
        return "\x1b[1;36m\u15E3\x1b[0m"
        
    def move(self, game_board, goal_pos):
        if self.cd > 0: 
            self.cd -= 1
            return
        if self.scared: goal_pos = self.home_pos
        min_dist = -1
        min_new_pos = self.pos
        for i in movement_array:
            new_pos = self.pos + i
            if game_board[new_pos.y][new_pos.x] == 1 or new_pos == self.last_pos: continue
            dist = new_pos.calc_distance(goal_pos)
            if min_dist == -1 or dist < min_dist:
                min_dist = dist
                min_new_pos = new_pos
        self.last_pos = self.pos
        self.pos = min_new_pos
    
class Clyde(Ghost): # Orange
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.home_pos = Pos(18,10)

    def get_sprite(self):
        if self.scared: return "\x1b[1;37m\u15E3\x1b[0m"
        return "\x1b[1;33m\u15E3\x1b[0m"
        
    def move(self, game_board, goal_pos):
        if self.cd > 0: 
            self.cd -= 1
            return
        if self.scared: goal_pos = self.home_pos
        min_dist = -1
        min_new_pos = self.pos
        for i in movement_array:
            new_pos = self.pos + i
            if game_board[new_pos.y][new_pos.x] == 1 or new_pos == self.last_pos: continue
            dist = new_pos.calc_distance(goal_pos)
            if min_dist == -1 or dist < min_dist:
                min_dist = dist
                min_new_pos = new_pos
        self.last_pos = self.pos
        self.pos = min_new_pos

class Pacman(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.dir = 1 # 0 up, 1 right, 2 down, 3 left
        self.move_dir = self.dir

    def get_sprite(self, current_frame: int) -> str:
        if current_frame % 2 == 0: return "\x1b[1;33m\u2296\x1b[0m"
        if self.move_dir == 0 or self.move_dir == 1: 
            return "\x1b[1;33m\u29C0\x1b[0m"
        else:
            return "\x1b[1;33m\u29C1\x1b[0m"
            
    def set_dir(self, dir: int) -> None:    
        self.dir = dir

    def move(self, game_board: list) -> None:
        new_pos = self.pos + movement_array[self.dir]
        if game_board[new_pos.y][new_pos.x] == 1:
            new_pos = self.pos + movement_array[self.move_dir]
            if game_board[new_pos.y][new_pos.x] == 1:
                return
            else: 
                self.pos = new_pos
        else: 
            self.move_dir = self.dir
            self.pos = new_pos

class Game:
    def __init__(self):
        self.kb = kb_input.KBHit()

        self.game_board = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1],
        [1, 2, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 2, 1],
        [1, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 1],
        [1, 2, 1, 2, 1, 1, 2, 1, 1, 0, 1, 1, 2, 1, 1, 2, 1, 2, 1],
        [1, 2, 3, 2, 2, 2, 2, 1, 0, 0, 0, 1, 2, 2, 2, 2, 3, 2, 1],
        [1, 2, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 2, 1],
        [1, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 1],
        [1, 2, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 2, 1],
        [1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]
        self.pacman = Pacman(9,7)
        self.score = 0
        self.ghosts = [Blinky(9,5), Pinky(8,5), Inky(10,5), Clyde(9,4)]
        self.frame_count = 0


    def run(self) -> None:
        # Game loop
        last_time = 0
        key_buffer = []
        scatter = True
        last_invun_frame = 0
        while True:
            # Keyboard input
            if self.kb.kbhit():
                c = self.kb.getch()
                key_buffer.append(c)

            current_time = time.time() * 1000
            if current_time - last_time >= 200:
                # Every 200ms
                last_time = current_time
                self.frame_count += 1
                if self.frame_count % 50 == 0:
                    scatter = not scatter
                for i in key_buffer:
                    if i == 'w': self.pacman.set_dir(0)
                    elif i == 'd': self.pacman.set_dir(1)
                    elif i == 's': self.pacman.set_dir(2)
                    elif i == 'a': self.pacman.set_dir(3)

                if self.frame_count - last_invun_frame >= 50:
                    for i in self.ghosts: i.scared = False

                self.pacman.move(self.game_board)
                if self.game_board[self.pacman.pos.y][self.pacman.pos.x] == 2:
                    self.score += 1
                    self.game_board[self.pacman.pos.y][self.pacman.pos.x] = 0
                elif self.game_board[self.pacman.pos.y][self.pacman.pos.x] == 3:
                    for i in self.ghosts: i.scared = True
                    self.score += 1
                    last_invun_frame = self.frame_count
                    self.game_board[self.pacman.pos.y][self.pacman.pos.x] = 0

                loss_flag = False
                for i in self.ghosts:
                    if self.pacman.pos == i.pos and not i.scared:
                        loss_flag = True
                        break
                    elif self.pacman.pos == i.pos and i.scared:
                        i.pos = Pos(9,5)
                        i.cd = 10
                        i.scared = False

                if loss_flag: break

                if not scatter:
                    self.ghosts[0].move(self.game_board, self.pacman.pos)
                    self.ghosts[1].move(self.game_board, self.pacman.pos + movement_array[self.pacman.move_dir] + movement_array[self.pacman.move_dir])
                    self.ghosts[2].move(self.game_board, self.pacman.pos + (self.pacman.pos - self.ghosts[0].pos))
                    if self.ghosts[3].pos.calc_distance(self.pacman.pos) > 64:
                        self.ghosts[3].move(self.game_board, self.pacman.pos)
                    else:
                        self.ghosts[3].move(self.game_board, self.ghosts[3].home_pos)
                else:
                    for i in self.ghosts:
                        i.move(self.game_board, i.home_pos)

                key_buffer = []
                self.render()

                loss_flag = False
                for i in self.ghosts:
                    if self.pacman.pos == i.pos and not i.scared:
                        loss_flag = True
                        break
                    elif self.pacman.pos == i.pos and i.scared:
                        i.pos = Pos(9,5)
                        i.cd = 10
                        i.scared = False

                if loss_flag: break

                if self.score == 96: # Max score
                    break

        if self.score == 96: print("You Win!")
        else: print("You Lost!")
        self.kb.set_normal_term()

    def render(self) -> None:
        output = "\x1b[H\x1b[0J"
        for i, e in enumerate(self.game_board):
            for j, sprite in enumerate(e):
                if j == self.pacman.pos.x and i == self.pacman.pos.y:
                    output += self.pacman.get_sprite(self.frame_count) + ' '
                else:
                    written_flag = False
                    for g in self.ghosts:
                        if j == g.pos.x and i == g.pos.y:
                            written_flag = True
                            output += g.get_sprite() + ' '
                            break
                    if not written_flag:
                        output += Game.get_sprite(sprite) + ' '
            output += '\n'
        output += f"Score: {self.score}" 
        print(output)

    def get_sprite(input: int) -> str:
        match input:
            case 0:
                return "\x1b[0m \x1b[0m"
            case 1:
                return "\x1b[1;34m#\x1b[0m"
            case 2:
                return "\x1b[1;37m·\x1b[0m"
            case 3:
                return "\x1b[1;37mo\x1b[0m"
            case _:
                return ""

def main() -> None:
    game = Game()
    game.run()

if __name__ == "__main__":
    main()