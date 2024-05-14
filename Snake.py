import pygame
import random
import pickle
import os

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Load sound effects
eat_sound = pygame.mixer.Sound("eating-sound-effect-36186.mp3")
game_over_sound = pygame.mixer.Sound("game-over-man-136233.mp3")

# Set up the screen
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20
GRID_WIDTH, GRID_HEIGHT = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 155, 0)
RED = (255, 0, 0)
DARK_RED = (155, 0, 0)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

# List of questions and answers
questions = [
    {"question": "What is the result of '2 + 3 * 4' in Python?", "answer": "14"},
    {"question": "What is the result of '3**2' in Python?", "answer": "9"},
    {"question": "What is the keyword used for creating a function in Python?", "answer": "def"},
    # Add more questions as needed
]

# Load or create leaderboard
def load_leaderboard():
    if os.path.exists('leaderboard.pkl'):
        with open('leaderboard.pkl', 'rb') as f:
            return pickle.load(f)
    else:
        return {}

# Save leaderboard
def save_leaderboard(leaderboard):
    with open('leaderboard.pkl', 'wb') as f:
        pickle.dump(leaderboard, f)

class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
        self.speed = 5  # Default speed

    def move(self):
        head = self.body[0]
        if self.direction == "UP":
            new_head = (head[0], head[1] - 1)
        elif self.direction == "DOWN":
            new_head = (head[0], head[1] + 1)
        elif self.direction == "LEFT":
            new_head = (head[0] - 1, head[1])
        elif self.direction == "RIGHT":
            new_head = (head[0] + 1, head[1])
        
        self.body.insert(0, new_head)
        self.body.pop()  # Remove the tail

    def grow(self):
        self.body.append(self.body[-1])

    def draw(self):
        for index, segment in enumerate(self.body):
            if index == 0:
                # Draw the head with eyes
                pygame.draw.circle(screen, GREEN, (segment[0] * CELL_SIZE + CELL_SIZE // 2, segment[1] * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2)
                # Draw eyes (two dots)
                eye_radius = 3
                left_eye_pos = (segment[0] * CELL_SIZE + CELL_SIZE // 3, segment[1] * CELL_SIZE + CELL_SIZE // 3)
                right_eye_pos = (segment[0] * CELL_SIZE + 2 * CELL_SIZE // 3, segment[1] * CELL_SIZE + CELL_SIZE // 3)
                pygame.draw.circle(screen, WHITE, left_eye_pos, eye_radius)
                pygame.draw.circle(screen, WHITE, right_eye_pos, eye_radius)
            else:
                # Draw the body segment
                pygame.draw.circle(screen, DARK_GREEN, (segment[0] * CELL_SIZE + CELL_SIZE // 2, segment[1] * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2)

# Food class
class Food:
    def __init__(self):
        self.position = self.generate_food_position()

    def generate_food_position(self):
        return random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1)

    def draw(self):
        pygame.draw.ellipse(screen, DARK_RED, (self.position[0] * CELL_SIZE, self.position[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.ellipse(screen, RED, (self.position[0] * CELL_SIZE + 2, self.position[1] * CELL_SIZE + 2, CELL_SIZE - 4, CELL_SIZE - 4))

# Obstacle class
class Obstacle:
    def __init__(self, level):
        self.positions = self.generate_obstacles(level)

    def generate_obstacles(self, level):
        num_obstacles = 5  # Easy level by default
        if 6 <= level <= 10:
            num_obstacles = 10  # Medium level
        elif level > 10:
            num_obstacles = 20  # Hard level

        positions = []
        while len(positions) < num_obstacles:
            position = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
            if position not in positions:
                positions.append(position)
        return positions

    def draw(self):
        for position in self.positions:
            pygame.draw.rect(screen, GRAY, (position[0] * CELL_SIZE, position[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Draw grid lines
def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (0, y), (WIDTH, y))

# Display main menu
def main_menu():
    # Load background image
    background_img = pygame.image.load("bg.png")
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

    # Font initialization
    font = pygame.font.Font(None, 50)

    # Button text and rect initialization
    play_text = font.render("PLAY", True, WHITE)
    play_rect = play_text.get_rect(center=(WIDTH // 2, HEIGHT // 1.5 - 5))
    leaderboard_text = font.render("LEADERBOARD", True, WHITE)
    leaderboard_rect = leaderboard_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 160))

    # Main menu loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if play_rect.collidepoint(x, y):
                    player_name = input_player_name()
                    main(player_name)  # Start the game with the player's name
                elif leaderboard_rect.collidepoint(x, y):
                    display_leaderboard()

        # Draw background image
        screen.blit(background_img, (0, 0))

        # Draw buttons with hover effect
        mouse_pos = pygame.mouse.get_pos()
        if play_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, DARK_GREEN, play_rect)
        else:
            pygame.draw.rect(screen, BLACK, play_rect)
        if leaderboard_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, DARK_GREEN, leaderboard_rect)
        else:
            pygame.draw.rect(screen, BLACK, leaderboard_rect)

        # Draw button text
        screen.blit(play_text, play_rect)
        screen.blit(leaderboard_text, leaderboard_rect)

        pygame.display.flip()

def input_player_name():
    # Load background image
    background_img = pygame.image.load("bg.png")
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

    # Font initialization
    font = pygame.font.Font(None, 50)
    
    # Input text initialization
    input_text = ""
    name_entered = False

    # Player name input loop
    while not name_entered:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and input_text:  # Ensure name is not empty
                    name_entered = True
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

        # Draw background image
        screen.blit(background_img, (0, 0))

        # Draw prompt text
        prompt_surface = font.render("Enter your name:", True, WHITE)
        screen.blit(prompt_surface, (WIDTH // 4, HEIGHT // 1.2 - 150))

        # Draw input text below the prompt
        input_surface = font.render(input_text, True, WHITE)
        screen.blit(input_surface, (WIDTH // 1.6, HEIGHT // 1.2 - 150))

        pygame.display.flip()

    return input_text

# Function to display try again button
def try_again(current_level):
    # Load background image
    background_img = pygame.image.load("bg.png")
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

    # Font initialization
    font = pygame.font.Font(None, 50)
    
    # Button text and rect initialization
    try_again_text = font.render("TRY AGAIN", True, WHITE)
    try_again_rect = try_again_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 200))

    # Try again button loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if try_again_rect.collidepoint(x, y):
                    main(current_level)
                    return

        # Draw background image
        screen.blit(background_img, (0, 0))

        # Draw try again button with hover effect
        mouse_pos = pygame.mouse.get_pos()
        if try_again_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, DARK_GREEN, try_again_rect)
        else:
            pygame.draw.rect(screen, BLACK, try_again_rect)

        # Draw button text
        screen.blit(try_again_text, try_again_rect)

        pygame.display.flip()

# Display leaderboard
def display_leaderboard():
    leaderboard = load_leaderboard()

    # Load background image
    background_img = pygame.image.load("grid_bg.png")
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

    # Font initialization
    font = pygame.font.Font(None, 40)
    title_font = pygame.font.Font(None, 60)

    # Leaderboard title initialization
    title_text = title_font.render("Leaderboard", True, WHITE)
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 250))

    # Sorted leaderboard by level
    sorted_leaderboard = sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)

    # Back button initialization
    back_text = font.render("BACK", True, WHITE)
    back_rect = back_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 300))

    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if back_rect.collidepoint(x, y):
                    running = False

        # Draw background image
        screen.blit(background_img, (0, 0))

        # Draw leaderboard title
        screen.blit(title_text, title_rect)

        # Draw top 10 players in leaderboard
        for i, (player, level) in enumerate(sorted_leaderboard[:10]):
            text = font.render(f"{player}: {level}", True, WHITE)
            screen.blit(text, (WIDTH // 2 - 100, HEIGHT // 2 - 200 + i * 40))

        # Draw back button with hover effect
        mouse_pos = pygame.mouse.get_pos()
        if back_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, DARK_GREEN, back_rect)
        else:
            pygame.draw.rect(screen, BLACK, back_rect)

        # Draw back button text
        screen.blit(back_text, back_rect)

        pygame.display.flip()

def main(player_name, level=1):
    snake = Snake()
    food = Food()
    current_level = 1
    clock = pygame.time.Clock()
    obstacles = Obstacle(current_level)

    def check_collision(pos):
        return (
            pos in snake.body[1:] or
            pos in obstacles.positions or
            pos[0] < 0 or pos[0] >= GRID_WIDTH or pos[1] < 0 or pos[1] >= GRID_HEIGHT
        )

    def display_question():
        question = random.choice(questions)
        question_text = question["question"]
        correct_answer = question["answer"]
        return question_text, correct_answer

    while True:
        screen.fill(BLACK)
        draw_grid()
        snake.draw()
        food.draw()
        obstacles.draw()

        # Display the player's name and the current level
        font = pygame.font.Font(None, 36)
        player_name_surface = font.render(f"Player: {player_name}", True, WHITE)
        level_surface = font.render(f"Level: {current_level}", True, WHITE)
        screen.blit(player_name_surface, (10, 10))
        screen.blit(level_surface, (10, 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != "DOWN":
                    snake.direction = "UP"
                elif event.key == pygame.K_DOWN and snake.direction != "UP":
                    snake.direction = "DOWN"
                elif event.key == pygame.K_LEFT and snake.direction != "RIGHT":
                    snake.direction = "LEFT"
                elif event.key == pygame.K_RIGHT and snake.direction != "LEFT":
                    snake.direction = "RIGHT"

        snake.move()
        if check_collision(snake.body[0]):
            game_over_sound.play()  # Play game over sound
            leaderboard = load_leaderboard()
            leaderboard[player_name] = max(leaderboard.get(player_name, 1), current_level)
            save_leaderboard(leaderboard)
            try_again(current_level)
            return

        if snake.body[0] == food.position:
            snake.grow()
            eat_sound.play()  # Play eat sound
            food.position = food.generate_food_position()
            question_text, correct_answer = display_question()

            font = pygame.font.Font(None, 36)
            input_box = pygame.Rect(100, 100, 140, 32)
            active = True
            user_text = ""
            while active:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            if user_text == correct_answer:
                                current_level += 1
                                obstacles = Obstacle(current_level)
                            active = False
                        elif event.key == pygame.K_BACKSPACE:
                            user_text = user_text[:-1]
                        else:
                            user_text += event.unicode

                screen.fill(BLACK)
                draw_grid()
                snake.draw()
                food.draw()
                obstacles.draw()
                question_surface = font.render(question_text, True, WHITE)
                screen.blit(question_surface, (10, 10))
                txt_surface = font.render(user_text, True, WHITE)
                width = max(200, txt_surface.get_width() + 10)
                input_box.w = width
                screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
                pygame.draw.rect(screen, WHITE, input_box, 2)
                pygame.display.flip()

        pygame.display.flip()
        clock.tick(snake.speed + current_level - 1)  # Increase speed with the level

if __name__ == "__main__":
    main_menu()
