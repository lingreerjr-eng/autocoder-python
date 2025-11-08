import pygame
import sys
import math
import random
from pygame.locals import *

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('3D Snake Game')

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

# Game settings
clock = pygame.time.Clock()
FPS = 60

# 3D Projection settings
fov = 256
viewer_distance = 4

class Point3D:
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z

    def project(self, width, height, fov, viewer_distance):
        """Convert 3D point to 2D point using perspective projection"""
        factor = fov / (viewer_distance + self.z)
        x = self.x * factor + width / 2
        y = -self.y * factor + height / 2
        return (x, y)

class Snake:
    def __init__(self):
        self.reset()
        self.speed = 0.1
        self.grow_pending = 0

    def reset(self):
        self.length = 3
        self.positions = [Point3D(0, 0, 0), Point3D(-0.5, 0, 0), Point3D(-1, 0, 0)]
        self.direction = (1, 0, 0)  # Moving right initially
        self.score = 0

    def move(self):
        head = self.positions[0]
        new_x = head.x + self.direction[0] * self.speed
        new_y = head.y + self.direction[1] * self.speed
        new_z = head.z + self.direction[2] * self.speed
        
        # Wrap around the play area
        if new_x > 10: new_x = -10
        if new_x < -10: new_x = 10
        if new_y > 10: new_y = -10
        if new_y < -10: new_y = 10
        if new_z > 10: new_z = -10
        if new_z < -10: new_z = 10
        
        new_head = Point3D(new_x, new_y, new_z)
        self.positions.insert(0, new_head)
        
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.positions.pop()

    def change_direction(self, direction):
        # Prevent 180-degree turns
        if (direction[0] * -1, direction[1] * -1, direction[2] * -1) != self.direction:
            self.direction = direction

    def grow(self):
        self.grow_pending += 1
        self.score += 10

    def check_collision(self):
        head = self.positions[0]
        for segment in self.positions[1:]:
            # Simple collision detection based on distance
            distance = math.sqrt((head.x - segment.x)**2 + 
                                (head.y - segment.y)**2 + 
                                (head.z - segment.z)**2)
            if distance < 0.3:
                return True
        return False

class Food:
    def __init__(self):
        self.position = Point3D(0, 0, 0)
        self.respawn()

    def respawn(self):
        self.position = Point3D(
            random.uniform(-8, 8),
            random.uniform(-8, 8),
            random.uniform(-8, 8)
        )

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        self.font = pygame.font.SysFont(None, 36)
        self.game_over = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if self.game_over and event.key == K_r:
                    self.restart()
                elif not self.game_over:
                    if event.key == K_UP or event.key == K_w:
                        self.snake.change_direction((0, 1, 0))
                    elif event.key == K_DOWN or event.key == K_s:
                        self.snake.change_direction((0, -1, 0))
                    elif event.key == K_LEFT or event.key == K_a:
                        self.snake.change_direction((-1, 0, 0))
                    elif event.key == K_RIGHT or event.key == K_d:
                        self.snake.change_direction((1, 0, 0))
                    elif event.key == K_q:
                        self.snake.change_direction((0, 0, 1))
                    elif event.key == K_e:
                        self.snake.change_direction((0, 0, -1))

    def update(self):
        if not self.game_over:
            self.snake.move()
            
            # Check food collision
            head = self.snake.positions[0]
            food_distance = math.sqrt((head.x - self.food.position.x)**2 + 
                                    (head.y - self.food.position.y)**2 + 
                                    (head.z - self.food.position.z)**2)
            if food_distance < 0.5:
                self.snake.grow()
                self.food.respawn()
            
            # Check self collision
            if self.snake.check_collision():
                self.game_over = True

    def draw(self, screen):
        screen.fill(BLACK)
        
        # Draw snake
        for i, pos in enumerate(self.snake.positions):
            # Make head larger and a different color
            size = 8 if i == 0 else 6
            color = YELLOW if i == 0 else GREEN
            projected = pos.project(WIDTH, HEIGHT, fov, viewer_distance)
            pygame.draw.circle(screen, color, (int(projected[0]), int(projected[1])), size)
        
        # Draw food
        food_projected = self.food.position.project(WIDTH, HEIGHT, fov, viewer_distance)
        pygame.draw.circle(screen, RED, (int(food_projected[0]), int(food_projected[1])), 7)
        
        # Draw score
        score_text = self.font.render(f'Score: {self.snake.score}', True, WHITE)
        screen.blit(score_text, (10, 10))
        
        # Draw game over message
        if self.game_over:
            game_over_text = self.font.render('GAME OVER! Press R to restart', True, WHITE)
            text_rect = game_over_text.get_rect(center=(WIDTH/2, HEIGHT/2))
            screen.blit(game_over_text, text_rect)
        
        # Draw instructions
        instructions = [
            "WASD: Move in X/Y plane",
            "Q/E: Move in Z-axis (forward/backward)",
            "R: Restart when game over"
        ]
        
        for i, instruction in enumerate(instructions):
            text = pygame.font.SysFont(None, 24).render(instruction, True, WHITE)
            screen.blit(text, (10, HEIGHT - 80 + i*25))

    def restart(self):
        self.snake.reset()
        self.food.respawn()
        self.game_over = False

def main():
    game = Game()
    
    while True:
        game.handle_events()
        game.update()
        game.draw(screen)
        
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
