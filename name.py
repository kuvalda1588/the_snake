"""Игра «Змейка» на Pygame."""
import random
import pygame

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTER_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

BOARD_BACKGROUND_COLOR = (0, 0, 0)
SNAKE_COLOR = (0, 255, 0)
APPLE_COLOR = (255, 0, 0)

UP = (0, -GRID_SIZE)
DOWN = (0, GRID_SIZE)
LEFT = (-GRID_SIZE, 0)
RIGHT = (GRID_SIZE, 0)


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position=CENTER_POSITION, body_color=(0, 0, 0)):
        """Инициализирует базовые атрибуты объекта."""
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """Абстрактный метод для отрисовки объекта."""
        pass

    def draw_cell(self, surface, position, color):
        """Отрисовывает одну ячейку на экране."""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, color, rect)


class Apple(GameObject):
    """Класс, описывающий яблоко."""

    def __init__(self):
        """Инициализирует яблоко."""
        super().__init__((0, 0), APPLE_COLOR)

    def randomize_position(self, occupied_positions):
        """Устанавливает случайное положение яблока."""
        all_cells = set(
            (x * GRID_SIZE, y * GRID_SIZE)
            for x in range(GRID_WIDTH)
            for y in range(GRID_HEIGHT)
        )
        free_cells = list(all_cells - set(occupied_positions))
        if free_cells:
            self.position = random.choice(free_cells)

    def draw(self, surface):
        """Отрисовывает яблоко на игровой поверхности."""
        self.draw_cell(surface, self.position, self.body_color)


class Snake(GameObject):
    """Класс, описывающий змейку."""

    def __init__(self):
        """Инициализирует змейку."""
        super().__init__(CENTER_POSITION, SNAKE_COLOR)
        self.length = 1
        self.positions = [self.position]
        self.direction = UP
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_x = (head_x + dx) % SCREEN_WIDTH
        new_y = (head_y + dy) % SCREEN_HEIGHT

        self.positions.insert(0, (new_x, new_y))

        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self, surface):
        """Отрисовывает змейку, затирая старый след."""
        if self.last:
            self.draw_cell(
                surface,
                self.last,
                BOARD_BACKGROUND_COLOR
            )
        self.draw_cell(
            surface,
            self.get_head_position(),
            self.body_color
        )

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [CENTER_POSITION]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None


def handle_keys(snake):
    """Обрабатывает нажатия клавиш для управления змейкой."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise SystemExit
            elif event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main():
    """Основной цикл игры."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('ЗМЕЙКА')
    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple()
    apple.randomize_position(snake.positions)

    while True:
        clock.tick(15)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            apple.randomize_position(snake.positions)

        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()