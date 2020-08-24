import pygame
import sys
import random

pygame.init()
WIDTH, HEIGHT = 500, 500
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
pygame.display.set_caption("Snake Game")
font = pygame.font.Font('freesansbold.ttf', 20)
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()


class Snake:
    def __init__(self, x, y, length, colour):
        self.body_parts = []
        self.valid = True
        self.x = x
        self.y = y
        self.length = length
        self.VEL = 25
        self.direction = 3
        self.width, self.height = 25, 25
        self.updateCount = 0
        self.updateCountMax = 11
        self.colour = colour
        for i in range(0, length):
            if i == 0:
                self.body_parts.append(SnakeBody(self.x, self.y, self.colour))
            else:
                self.body_parts.append(SnakeBody(self.x, self.body_parts[0].y + self.width, self.colour))

    def update(self):
        self.updateCount = self.updateCount + 1
        if self.updateCount >= self.updateCountMax:

            for i in range(len(self.body_parts) - 1, 0, -1):
                self.body_parts[i].x = self.body_parts[i - 1].x
                self.body_parts[i].y = self.body_parts[i - 1].y

            self.move()
            self.updateCount = 0

    def draw(self, window):
        for parts in self.body_parts:
            parts.draw(window)

    def move(self):
        if self.direction == 0:  # WEST
            self.body_parts[0].x = self.body_parts[0].x - self.VEL
        elif self.direction == 1:  # EAST
            self.body_parts[0].x = self.body_parts[0].x + self.VEL
        elif self.direction == 3:  # NORTH
            self.body_parts[0].y = self.body_parts[0].y - self.VEL
        elif self.direction == 2:  # SOUTH
            self.body_parts[0].y = self.body_parts[0].y + self.VEL


class Player(Snake):
    def __init__(self, x, y, length):
        super().__init__(x, y, length, "red")

    def update(self):
        self.updateCount = self.updateCount + 1
        if self.updateCount >= self.updateCountMax:

            for i in range(len(self.body_parts) - 1, 0, -1):
                self.body_parts[i].x = self.body_parts[i - 1].x
                self.body_parts[i].y = self.body_parts[i - 1].y

            if self.length in [11, 16, 21]:
                self.valid = True

            if self.length in [10, 15, 20, 25] and self.valid:
                self.increment_velocity()
                self.valid = False
            self.move()
            self.updateCount = 0

    def increment_velocity(self):
        self.updateCount -= 1

    def eat(self, obj, game):
        game.remove(obj)
        self.add_part()

    def add_part(self):
        self.length += 1
        self.body_parts.append(SnakeBody(self.body_parts[len(self.body_parts) - 1].x + self.width,
                                         self.body_parts[len(self.body_parts) - 1].y, "red"))


class Computer(Snake):
    def __init__(self, x, y, length):
        super().__init__(x, y, length, "blue")
        self.updateCountMax = 60

    def target(self, dx, dy):
        # print("dx,dy,x,y: {},{},{},{}  direction: {}".format(dx, dy, self.body_parts[0].x, self.body_parts[0].y,
        #                                                      self.direction))
        if self.body_parts[0].x > dx:
            self.direction = 0
        if self.body_parts[0].x < dx:
            self.direction = 1

        if -30 < self.body_parts[0].x - dx < 30:
            if self.body_parts[0].y > dy:
                self.direction = 3
            if self.body_parts[0].y < dy:
                self.direction = 2


class SnakeBody:
    def __init__(self, x, y, colour):
        self.x = x
        self.y = y
        self.width, self.height = 25, 25
        self.img = pygame.Rect(self.x, self.y, self.width, self.height)
        if colour == "red":
            self.colour = (255, 0, 0)
        elif colour == "blue":
            self.colour = (0, 0, 255)

    def draw(self, window):
        self.img = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(window, self.colour, self.img)


class Food:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width, self.height = 25, 25
        self.img = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, window):
        self.img = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(window, (0, 255, 0), self.img)


def draw_grid(width, rows, window):
    sizeBtwn = width // rows
    print(sizeBtwn)
    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn
        pygame.draw.line(window, (255, 255, 255), (x, 0), (x, width))
        pygame.draw.line(window, (255, 255, 255), (0, y), (width, y))


def main():
    ####################################################################################
    # Initialise
    ROWS = 20
    run = True
    player = Player(25 * 3, 25 * 15, 4)
    computer = Computer(350, 100, 3)
    score = 0
    numFood = 1
    game = []
    randx = random.randint(0, ROWS)
    randy = random.randint(0, ROWS)
    food = Food(25*randx, 25*randy)
    game.append(food)
    game.append(player)
    game.append(computer)
    while run:
        ####################################################################################
        # Setup
        CLOCK.tick(60)
        count = 0

        ####################################################################################
        # Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        for key in keys:
            if key:
                count += 1
        check = count == 1

        if check:
            if keys[pygame.K_RIGHT] and not player.direction == 0:
                player.direction = 1
            elif keys[pygame.K_LEFT] and not player.direction == 1:
                player.direction = 0
            elif keys[pygame.K_UP] and not player.direction == 2:
                player.direction = 3
            elif keys[pygame.K_DOWN] and not player.direction == 3:
                player.direction = 2

        scores = font.render(f"Score: {score}", True, WHITE, BLACK)
        ####################################################################################
        # Game mechanics
        while numFood < 1:
            randx = random.randint(0, ROWS - 2)
            randy = random.randint(0, ROWS - 2)
            numFood += 1
            # print("food placed at ({},{})".format(randx, randy))
            food = Food(25*randx, 25*randy)
            game.append(food)

        for obj in game:
            if isinstance(obj, Food):
                if player.body_parts[0].img.colliderect(obj.img) and obj in game:
                    numFood -= 1
                    score += 1
                    player.eat(obj, game)

        ####################################################################################
        # Game exit conditions
        for i in range(1, len(player.body_parts)):
            if player.body_parts[0].img.colliderect(player.body_parts[i].img) and i != 0:
                run = False

        for obj in game:
            if isinstance(obj, Computer):
                for i in range(0, len(player.body_parts)):
                    for j in range(0, len(computer.body_parts)):
                        if player.body_parts[i].img.colliderect(computer.body_parts[j].img) and obj in game:
                            run = False

        if (not (0 <= player.body_parts[0].x <= WIDTH - player.width)) or (
                not (0 <= player.body_parts[0].y <= HEIGHT - player.height)):
            run = False
        ####################################################################################
        # Updates and Drawings
        computer.target(player.body_parts[0].x, player.body_parts[0].y)
        player.update()
        computer.update()
        pygame.draw.rect(SCREEN, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
        for objects in game:
            objects.draw(SCREEN)
        draw_grid(WIDTH, ROWS, SCREEN)
        SCREEN.blit(scores, (10, 10))
        pygame.display.update()


def main_menu():
    title_font = pygame.font.SysFont("comicsans", 35)
    while True:
        pygame.draw.rect(SCREEN, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
        title = title_font.render(f"Press space to begin...", True, WHITE, BLACK)
        SCREEN.blit(title, (WIDTH / 2 - title.get_width() / 2, HEIGHT // 2))
        pygame.display.update()

        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        if keys[pygame.K_SPACE]:
            main()
            pygame.time.wait(1000)


if __name__ == "__main__":
    main_menu()
