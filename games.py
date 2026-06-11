import pygame
import random

pygame.init()
WIDTH, HEIGHT = 400, 300
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (135, 206, 235)
GREEN = (0, 170, 0)
RED = (255, 0, 0)
YELLOW = (255, 215, 0)
GRAY = (102, 102, 102)

class FlappyBird:
    def __init__(self):
        self.bird_x, self.bird_y = 50, HEIGHT // 2
        self.velocity = 0
        self.pipes = []
        self.score = 0
        self.running = True

    def handle_event(self, event):
        if event.type in [pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN]:
            self.velocity = -6

    def update(self):
        self.velocity += 0.4
        self.bird_y += self.velocity
        if not self.pipes or self.pipes[-1][0] < WIDTH - 100:
            gap = random.randint(50, HEIGHT - 170)
            self.pipes.append([WIDTH, gap, gap + 120])
        
        for pipe in self.pipes[:]:
            pipe[0] -= 3
            if pipe[0] < -50:
                self.pipes.remove(pipe)
                self.score += 1
            if 40 < pipe[0] < 90 and (self.bird_y < pipe[1] or self.bird_y + 20 > pipe[2]):
                self.running = False
        
        if self.bird_y > HEIGHT or self.bird_y < 0:
            self.running = False

    def draw(self, screen):
        screen.fill(BLUE)
        pygame.draw.rect(screen, YELLOW, (self.bird_x, self.bird_y, 20, 20))
        for pipe in self.pipes:
            pygame.draw.rect(screen, GREEN, (pipe[0], 0, 50, pipe[1]))
            pygame.draw.rect(screen, GREEN, (pipe[0], pipe[2], 50, HEIGHT - pipe[2]))

class Snake:
    def __init__(self):
        self.snake = [(WIDTH // 2, HEIGHT // 2)]
        self.food = (random.randint(0, WIDTH // 20) * 20, random.randint(0, HEIGHT // 20) * 20)
        self.direction = (1, 0)
        self.next_dir = (1, 0)
        self.score = 0
        self.running = True

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            keys = {pygame.K_UP: (0, -1), pygame.K_DOWN: (0, 1), pygame.K_LEFT: (-1, 0), pygame.K_RIGHT: (1, 0)}
            if event.key in keys:
                self.next_dir = keys[event.key]

    def update(self):
        self.direction = self.next_dir
        new_head = (self.snake[0][0] + self.direction[0] * 20, self.snake[0][1] + self.direction[1] * 20)
        
        if not (0 <= new_head[0] < WIDTH and 0 <= new_head[1] < HEIGHT) or new_head in self.snake:
            self.running = False
            return
        
        self.snake.insert(0, new_head)
        if new_head == self.food:
            self.score += 1
            self.food = (random.randint(0, WIDTH // 20) * 20, random.randint(0, HEIGHT // 20) * 20)
        else:
            self.snake.pop()

    def draw(self, screen):
        screen.fill(BLACK)
        for segment in self.snake:
            pygame.draw.rect(screen, (0, 255, 0), (segment[0], segment[1], 20, 20))
        pygame.draw.rect(screen, RED, (self.food[0], self.food[1], 20, 20))

class Memory:
    def __init__(self):
        self.cards = []
        self.flipped = []
        self.matched = 0
        self.score = 0
        self.running = True
        values = list(range(6)) * 2
        random.shuffle(values)
        for i in range(4):
            for j in range(3):
                self.cards.append({'x': i * 70 + 20, 'y': j * 70 + 20, 'value': values[i + j * 4], 'flipped': False})

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and len(self.flipped) < 2:
            x, y = pygame.mouse.get_pos()
            for idx, card in enumerate(self.cards):
                if card['x'] < x < card['x'] + 60 and card['y'] < y < card['y'] + 60:
                    if not card['flipped'] and idx not in self.flipped:
                        card['flipped'] = True
                        self.flipped.append(idx)
                        if len(self.flipped) == 2:
                            if self.cards[self.flipped[0]]['value'] == self.cards[self.flipped[1]]['value']:
                                self.matched += 1
                                self.score += 1
                                self.flipped = []
                                if self.matched == 6:
                                    self.running = False
                            else:
                                pygame.time.set_timer(pygame.USEREVENT, 800)

    def update(self):
        pass

    def draw(self, screen):
        screen.fill(BLACK)
        for card in self.cards:
            color = YELLOW if card['flipped'] else GRAY
            pygame.draw.rect(screen, color, (card['x'], card['y'], 60, 60))
            pygame.draw.rect(screen, WHITE, (card['x'], card['y'], 60, 60), 2)
            if card['flipped']:
                font = pygame.font.Font(None, 36)
                text = font.render(str(card['value']), True, BLACK)
                screen.blit(text, (card['x'] + 18, card['y'] + 15))

def run_game(game_class, title):
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(title)
    clock = pygame.time.Clock()
    game = game_class()
    while game.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            game.handle_event(event)
        game.update()
        game.draw(screen)
        pygame.display.flip()
        clock.tick(10 if isinstance(game, Snake) else 60)
    print(f"Score: {game.score}")
    pygame.time.wait(2000)

if __name__ == '__main__':
    print("Wähle ein Spiel: 1=Flappy Bird, 2=Snake, 3=Memory")
    choice = input("Auswahl: ")
    if choice == '1': run_game(FlappyBird, "Flappy Bird")
    elif choice == '2': run_game(Snake, "Snake")
    elif choice == '3': run_game(Memory, "Memory")
    pygame.quit()