import pygame
import math
import heapq

pygame.init()

# Screen dimensions
width, height = 800, 600
grid_size = 20

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Differential Drive Robot Simulation with A* Pathfinding")

# Colors
black = (0, 0, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)
gray = (100, 100, 100)
green = (0, 255, 0)

# Load and scale car image
car_image = pygame.image.load("car.png")
car_image = pygame.transform.scale(car_image, (80, 81))  # match true size

SPEED = 20

obstacles = [
    pygame.Rect(200, 150, 100, 300),
    pygame.Rect(400, 100, 50, 400),
    pygame.Rect(600, 200, 100, 100)
]


class Robot:
    def __init__(self, x, y, size, wheel_radius, wheel_base):
        self.x = x
        self.y = y
        self.angle = 0
        self.left_wheel_speed = 0
        self.right_wheel_speed = 0
        self.size = size
        self.wheel_radius = wheel_radius
        self.wheel_base = wheel_base
        self.image = car_image
        self.path = []

    def draw(self, screen):
        if len(self.path) > 1:
            pygame.draw.lines(screen, red, False, self.path, 2)
        rotated_image = pygame.transform.rotate(self.image, -math.degrees(self.angle))
        rect = rotated_image.get_rect(center=(self.x, self.y))
        screen.blit(rotated_image, rect.topleft)

    def update(self, dt):
        v_left = self.left_wheel_speed * self.wheel_radius
        v_right = self.right_wheel_speed * self.wheel_radius
        v = (v_left + v_right) / 2
        omega = (v_right - v_left) / self.wheel_base

        self.x += v * math.cos(self.angle) * dt
        self.y += v * math.sin(self.angle) * dt
        self.angle += omega * dt

        self.path.append((self.x, self.y))
        if len(self.path) > 1000:
            self.path.pop(0)

    def set_wheel_speeds(self, left, right):
        self.left_wheel_speed = left
        self.right_wheel_speed = right


def draw_obstacles(screen):
    for obs in obstacles:
        pygame.draw.rect(screen, gray, obs)


def is_blocked(x, y):
    return any(obs.colliderect(pygame.Rect(x, y, grid_size, grid_size)) for obs in obstacles)


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(start, goal):
    start = (start[0] // grid_size, start[1] // grid_size)
    goal = (goal[0] // grid_size, goal[1] // grid_size)
    open_set = [(0, start)]
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            path = [(goal[0] * grid_size + grid_size // 2, goal[1] * grid_size + grid_size // 2)]
            while current in came_from:
                cx, cy = current
                path.append((cx * grid_size + grid_size // 2, cy * grid_size + grid_size // 2))
                current = came_from[current]
            path.reverse()
            return path
        for dx, dy in directions:
            neighbor = (current[0] + dx, current[1] + dy)
            nx, ny = neighbor
            if 0 <= nx < width // grid_size and 0 <= ny < height // grid_size:
                if is_blocked(nx * grid_size, ny * grid_size):
                    continue
                tentative_g = g_score[current] + 1
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
    return []


def draw_path(screen, path):
    if path:
        pygame.draw.lines(screen, yellow, False, path, 3)


# Initialize robot and path
start_pos = (100, 100)
goal_pos = (700, 500)
robot = Robot(*start_pos, 20, 5, 40)
astar_path = astar(start_pos, goal_pos)

clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                robot.set_wheel_speeds(-SPEED, SPEED)
            elif event.key == pygame.K_RIGHT:
                robot.set_wheel_speeds(SPEED, -SPEED)
            elif event.key == pygame.K_UP:
                robot.set_wheel_speeds(SPEED, SPEED)
            elif event.key == pygame.K_DOWN:
                robot.set_wheel_speeds(-SPEED, -SPEED)
        elif event.type == pygame.KEYUP:
            robot.set_wheel_speeds(0, 0)

    dt = clock.tick(60) / 1000.0
    robot.update(dt)

    screen.fill(black)
    draw_obstacles(screen)
    draw_path(screen, astar_path)
    pygame.draw.circle(screen, green, goal_pos, 20)
    robot.draw(screen)
    pygame.display.flip()

pygame.quit()
