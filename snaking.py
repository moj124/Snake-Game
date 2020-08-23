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


class Player:
    def __init__(self, x, y, length):
        self.body_parts = []
        self.valid = True
        self.x = x
        self.y = y
        self.length = length
        self.VEL = 21
        self.direction = 3
        self.width, self.height = 20, 20
        self.updateCount = 0
        self.updateCountMax = 11
        for i in range(0, length):
            if i == 0:
                self.body_parts.append(SnakeBody(self.x, self.y))
            else:
                self.body_parts.append(SnakeBody(self.x, self.body_parts[0].y + self.width))

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

    def add_part(self):
        self.length += 1
        self.body_parts.append(SnakeBody(self.body_parts[len(self.body_parts) - 1].x + self.width,
                                         self.body_parts[len(self.body_parts) - 1].y))

    def increment_velocity(self):
        self.updateCount -= 1


class SnakeBody:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width, self.height = 20, 20
        self.img = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, window):
        self.img = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(window, (255, 0, 0), self.img)


class Food:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width, self.height = 20, 20
        self.img = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, window):
        self.img = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(window, (0, 255, 0), self.img)


def main():
    ####################################################################################
    # Initialise
    run = True
    player = Player(WIDTH // 2, HEIGHT // 2, 4)
    score = 0
    numFood = 1
    game = []
    randx = random.randint(0, WIDTH - 50)
    randy = random.randint(0, HEIGHT - 50)
    food = Food(randx, randy)
    game.append(food)
    game.append(player)
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
            randx = random.randint(0, WIDTH - 50)
            randy = random.randint(0, HEIGHT - 50)
            numFood += 1
            # print("food placed at ({},{})".format(randx, randy))
            food = Food(randx, randy)
            game.append(food)

        for obj in game:
            if isinstance(obj, Food):
                if player.body_parts[0].img.colliderect(obj.img) and obj in game:
                    numFood -= 1
                    score += 1
                    game.remove(obj)
                    player.add_part()

        ####################################################################################
        # Game exit conditions
        for i in range(1, len(player.body_parts)):
            if player.body_parts[0].img.colliderect(player.body_parts[i].img) and i != 0:
                run = False

        if (not (0 <= player.body_parts[0].x <= WIDTH - player.width)) or (
                not (0 <= player.body_parts[0].y <= HEIGHT - player.height)):
            run = False
        ####################################################################################
        # Updates and Drawings
        player.update()
        pygame.draw.rect(SCREEN, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
        SCREEN.blit(scores, (10, 10))
        for objects in game:
            objects.draw(SCREEN)
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
            print("working")


if __name__ == "__main__":
    main_menu()