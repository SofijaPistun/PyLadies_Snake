from random import randrange
from colorama import init, Fore, Back, Style

# Initializes Colorama
init(autoreset=True)

class GameSnake:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.board = []
        self.head = (1, 3)
        self.way = 'd'
        self.move = [0, 0]
        self.food = (0, 0)
        head_temp = list(self.head)
        self.snake = {
            0: self.head,
            1: tuple((head_temp[0], head_temp[1] - 1)),
            2: tuple((head_temp[0], head_temp[1] - 2))
        }
        self.game_over_b = False
        self.symbol_snake = 'O'
        self.symbol_food = '@'
        self.symbol_border_top = '#'
        self.symbol_border_bottom = '#'
        self.symbol_border_right = '|'
        self.symbol_border_left = '|'
        self.symbol_board = ' '
        self.symbol_crash = 'X'

    def create_empty_board(self):
        board = []
        zero_row = []
        last_row = []
        
        for i in range(self.y + 1):
            zero_row.append(self.symbol_border_top)
            last_row.append(self.symbol_border_bottom)
        board.append(zero_row)
        
        for i in range(self.x):
            row = []
            for j in range(self.y):
                if j == 0:
                    row.append(self.symbol_border_left)
                else:
                    row.append(self.symbol_board)
                if j == (self.y - 1):
                    row.append(self.symbol_border_right)
            board.append(row)        

        board.append(last_row)
        self.board = board

    def print_board(self):
        for row in self.board:
            for element in row:
                if not self.game_over_b:
                    if element == self.symbol_snake:
                        print(Back.BLUE + Fore.GREEN + Style.BRIGHT + f"{element}", end="")    
                    elif element == self.symbol_food:
                        print(Back.BLUE + f"{element}", end="") 
                    elif element == self.symbol_crash:
                        print(Back.BLUE + Fore.RED + f"{element}", end="")
                    elif element == self.symbol_border_top or element == self.symbol_border_bottom or element == self.symbol_border_left or element == self.symbol_border_right:
                        print(Fore.YELLOW + f"{element}", end="")
                    elif element == self.symbol_board:
                        print(Back.BLUE + f"{element}", end="")
                    else:
                        print(f"{element}", end="")
                else:                    
                    if element == self.symbol_food:
                        print(Fore.RED + f"{element}", end="") 
                    elif element == self.symbol_crash:
                        print(Fore.RED + f"{element}", end="")
                    elif element == self.symbol_border_top or element == self.symbol_border_bottom or element == self.symbol_border_left or element == self.symbol_border_right:
                        print(Fore.RED + f"{element}", end="")
                    elif element == self.symbol_board:
                        print(Back.BLACK + f"{element}", end="")
                    else:
                        print(f"{element}", end="")
            print()    

    def create_food_for_snake(self):
        while(True):
            food_temp = []
            food_temp.append(randrange(1, self.x - 1))
            food_temp.append(randrange(1, self.y - 1))
            #print(f'food_temp = {food_temp}')
            if not (tuple(food_temp) in self.snake.values()):
                self.food = tuple(food_temp)
                break
    
    def move_snake(self):
        while(True):
            self.way = input('What is the snake\'s next move? The snake can move right (d), left (a), up (w) or down (s). Or you can end the game (end). ')
            if self.way.lower() == 'd':
                self.move = [0, 1] 
            elif self.way.lower() == 'a':
                self.move = [0, -1]
            elif self.way.lower() == 'w':
                self.move = [-1, 0]
            elif self.way.lower() == 's':
                self.move = [1, 0]
            else:
                continue
            
            head_temp = list(self.head)
            head_temp[0] = head_temp[0] + self.move[0]
            head_temp[1] = head_temp[1] + self.move[1]
            self.head = tuple(head_temp)

            self.game_over()
            if self.game_over_b:
                self.draw_snake_and_food_on_board()
                game_over = ' ' * ((self.y - len('Game over'))//2) + ' GAME OVER ' + ' ' * ((self.y - len('Game over'))//2)
                print(Back.RED + Fore.WHITE + game_over)
                self.print_board()
                break
            else:                        
                if self.head == self.food:
                    snake_temp = {
                        0: self.head
                    }
                    for i in self.snake:
                        snake_temp[i + 1] = self.snake[i]
                    self.snake.clear()
                    self.snake = snake_temp.copy()

                    self.draw_snake_and_food_on_board()
                    self.create_food_for_snake()            
                else:
                    snake_temp = {
                        0: self.head
                    }
                    for i in self.snake:
                        if i != (len(self.snake) - 1):
                            snake_temp[i + 1] = self.snake[i]
                    self.snake.clear()
                    self.snake = snake_temp.copy()

                self.create_empty_board()
                self.draw_snake_and_food_on_board()
                self.print_board()

            if self.way == 'end':
                break
        
    def draw_snake_and_food_on_board(self):
        self.board[self.food[0]][self.food[1]] = self.symbol_food
        snake_temp = list(self.snake.values())
        for i in snake_temp:
            j = list(i)
            self.board[j[0]][j[1]] = self.symbol_snake

        if self.game_over_b:
            snake_temp = list(self.snake.values())
            for i in snake_temp:
                j = list(i)
                self.board[j[0]][j[1]] = self.symbol_crash
            
    def game_over(self):
        if self.head[0] == 0 or self.head[0] == (self.x + 1) or self.head[1] == 0 or self.head[1] == self.y:
            self.game_over_b = True
        elif self.head in self.snake.values():
            self.game_over_b = True

    def start_game(self):
        while(True):           
            print('Enter the size for the game board: ') 
            y = input('Horizontal (between 4..50, recommend value 25): ')
            x = input('Vertical (between 4..25, recommend value 15): ')
            if x != '' and y != '':
                self.x = int(x)
                self.y = int(y) + 1
                if 4 <= self.x <=25 and 4 <= self.y <= 50:
                    start_str = ' ' * ((self.y - len('Snake'))//2) + ' SNAKE ' + ' ' * ((self.y - len('Snake'))//2)
                    print(Back.BLUE + Fore.WHITE + start_str)                
                    break
                else:
                    print('Size for the board is incorrect. Try again.')
            else:
                continue

    def game(self):
        self.start_game()
        self.create_empty_board()
        self.create_food_for_snake()
        self.draw_snake_and_food_on_board()
        self.print_board()
        self.move_snake()        

snake = GameSnake()
snake.game()




