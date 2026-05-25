import pygame
import heapq
import random
import time
import threading
import requests

# --- Setup & Configuration ---
WIDTH, HEIGHT = 600, 600
ROWS = 25
GRID_SIZE = WIDTH // ROWS
FPS = 15

# --- Colors ---
ASPHALT = (42, 45, 49)
ROAD_LINE = (230, 230, 230)
AGENT_COLORS = [(41, 128, 185), (155, 89, 182), (230, 126, 34)] # Blue, Purple, Orange
TREE_LEAVES = (39, 174, 96)
TREE_SHADOW = (20, 90, 50)
CONE_ORANGE = (230, 126, 34)
CONE_WHITE = (236, 240, 241)
PED_SHIRT = (192, 57, 43)
PED_HEAD = (241, 196, 15)
PARKED_CAR_COLORS = [(149, 165, 166), (52, 73, 94), (22, 160, 133)]
DYNAMIC_ALERT = (241, 196, 15)

global_logs = []

def add_log(msg):
    global global_logs
    global_logs.append(msg)
    if len(global_logs) > 30:
        global_logs.pop(0)

class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x = col * GRID_SIZE
        self.y = row * GRID_SIZE
        self.is_obstacle = False
        self.obs_type = None 
        self.car_color = None
        self.is_dynamic = False
        self.neighbors = []

    def make_obstacle(self, obs_type, dynamic=False):
        self.is_obstacle = True
        self.obs_type = obs_type
        self.is_dynamic = dynamic
        if obs_type == "car":
            self.car_color = random.choice(PARKED_CAR_COLORS)
            
    def clear(self):
        self.is_obstacle = False
        self.obs_type = None
        self.is_dynamic = False

    def draw(self, win):
        center_x = self.x + GRID_SIZE // 2
        center_y = self.y + GRID_SIZE // 2
        
        if self.is_obstacle:
            if self.obs_type != "pedestrian":
                pygame.draw.circle(win, (25, 25, 25), (center_x + 3, center_y + 3), GRID_SIZE//2 - 2)

            if self.obs_type == "tree":
                pygame.draw.circle(win, TREE_SHADOW, (center_x, center_y), GRID_SIZE // 2)
                pygame.draw.circle(win, TREE_LEAVES, (center_x - 3, center_y - 3), int(GRID_SIZE * 0.35))
                pygame.draw.circle(win, (46, 204, 113), (center_x + 2, center_y + 1), int(GRID_SIZE * 0.25))
            elif self.obs_type == "cone":
                base_w = GRID_SIZE - 12
                pygame.draw.rect(win, CONE_ORANGE, (self.x + 6, self.y + GRID_SIZE - 8, base_w, 4), border_radius=2)
                pygame.draw.polygon(win, CONE_ORANGE, [(self.x + 8, self.y + GRID_SIZE - 8), (self.x + GRID_SIZE - 8, self.y + GRID_SIZE - 8), (center_x, self.y + 6)])
                pygame.draw.polygon(win, CONE_WHITE, [(self.x + 10, self.y + GRID_SIZE - 14), (self.x + GRID_SIZE - 10, self.y + GRID_SIZE - 14), (center_x, self.y + 12)])
            elif self.obs_type == "pedestrian":
                pygame.draw.ellipse(win, PED_SHIRT, (self.x + 6, center_y - 4, GRID_SIZE - 12, 10))
                pygame.draw.circle(win, PED_HEAD, (center_x, center_y), 6)
            elif self.obs_type == "car":
                draw_top_down_car(win, self.x, self.y, self.car_color, (0, -1)) 

            if self.is_dynamic:
                pygame.draw.rect(win, DYNAMIC_ALERT, (self.x, self.y, GRID_SIZE, GRID_SIZE), 2, border_radius=4)

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < ROWS - 1 and not grid[self.row + 1][self.col].is_obstacle:
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].is_obstacle:
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < ROWS - 1 and not grid[self.row][self.col + 1].is_obstacle:
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].is_obstacle:
            self.neighbors.append(grid[self.row][self.col - 1])

def draw_top_down_car(win, x, y, color, direction):
    dx, dy = direction
    w = GRID_SIZE - 8
    h = GRID_SIZE - 2
    
    rect = pygame.Rect(0, 0, w, h)
    rect.center = (x + GRID_SIZE//2, y + GRID_SIZE//2)
    
    if dx != 0: 
        rect.width, rect.height = h, w
        rect.center = (x + GRID_SIZE//2, y + GRID_SIZE//2)
        
    pygame.draw.rect(win, (20,20,20), rect, border_radius=4) 
    pygame.draw.rect(win, color, rect.inflate(-2, -2), border_radius=4)
    
    glass = pygame.Rect(0, 0, w - 4, 6)
    if dx == 1:   
        glass.width, glass.height = 6, w - 4
        glass.center = (rect.right - 8, rect.centery)
    elif dx == -1: 
        glass.width, glass.height = 6, w - 4
        glass.center = (rect.left + 8, rect.centery)
    elif dy == 1:  
        glass.center = (rect.centerx, rect.bottom - 8)
    else:          
        glass.center = (rect.centerx, rect.top + 8)

    pygame.draw.rect(win, (135, 206, 235), glass, border_radius=1) 

def heuristic(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def a_star(grid, start, end):
    count = 0
    open_set = []
    heapq.heappush(open_set, (0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = heuristic((start.row, start.col), (end.row, end.col))
    open_set_hash = {start}

    while open_set:
        current = heapq.heappop(open_set)[2]
        open_set_hash.remove(current)

        if current == end:
            path = []
            while current in came_from:
                current = came_from[current]
                path.append(current)
            return path[::-1]

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic((neighbor.row, neighbor.col), (end.row, end.col))
                if neighbor not in open_set_hash:
                    count += 1
                    heapq.heappush(open_set, (f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
    return []

def draw_background(win):
    win.fill(ASPHALT)
    for i in range(ROWS):
        pygame.draw.line(win, (55, 60, 65), (0, i * GRID_SIZE), (WIDTH, i * GRID_SIZE))
        pygame.draw.line(win, (55, 60, 65), (i * GRID_SIZE, 0), (i * GRID_SIZE, HEIGHT))
    for i in range(4, ROWS, 4):
        for j in range(0, ROWS, 2):
            pygame.draw.rect(win, (200, 200, 200), (j * GRID_SIZE + GRID_SIZE//4, i * GRID_SIZE, GRID_SIZE//2, 2))

class Agent:
    def __init__(self, start_node, end_node, color, name_id):
        self.name_id = name_id
        self.current_node = start_node
        self.end_node = end_node
        self.color = color
        self.path = []
        self.path_index = 0
        self.robot_dir = (0, 1)
        self.status = "Initializing..."
        
        self.target_speed = 45.0
        self.current_speed = 0.0
        self.distance = 200

        start_node.clear()
        end_node.clear()

def send_telemetry_loop(agents):
    while True:
        try:
            main_agent = agents[0] # Connect dashboard to Agent 0
            
            # Smooth speed transition for dashboard
            main_agent.current_speed += (main_agent.target_speed - main_agent.current_speed) * 0.2
            
            status_text = "AUTOPILOT ENGAGED"
            status_color = "var(--accent-green)"
            dist_render = main_agent.distance

            if main_agent.target_speed == 0:
                status_text = "EMERGENCY BRAKE / YIELDING"
                status_color = "var(--accent-red)"
            elif main_agent.target_speed < 30:
                status_text = "OBSTACLE DETECTED"
                status_color = "#f1c40f"
                
            payload = {
                "sys_status": status_text,
                "status_color": status_color,
                "speed": main_agent.current_speed,
                "distance": dist_render,
                "fps": FPS,
                "ping": random.randint(10, 20),
                "logs": global_logs[-10:],
                "tracker_coords": f"X:{main_agent.current_node.col*GRID_SIZE} Y:{main_agent.current_node.row*GRID_SIZE}",
                "obj_count": len(agents) + 3 # Fake metric
            }
            requests.post("http://127.0.0.1:5000/update_telemetry", json=payload, timeout=0.1)
        except:
            pass # Silently fail if Flask isn't up
        time.sleep(0.1)

def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Multi-Agent Autonomous Navigation Proving Grounds")
    font = pygame.font.SysFont("Trebuchet MS", 14, bold=True)
    
    grid = [[Node(i, j) for j in range(ROWS)] for i in range(ROWS)]
    
    # Spawn Static Obstacles
    obstacle_types = ["tree", "tree", "cone", "pedestrian", "car", "car"]
    num_obstacles = int((ROWS * ROWS) * 0.15)
    for _ in range(num_obstacles):
        r = random.randint(0, ROWS - 1)
        c = random.randint(0, ROWS - 1)
        grid[r][c].make_obstacle(random.choice(obstacle_types))
        
    for row in grid:
        for node in row:
            node.update_neighbors(grid)

    # Spawn Multiple Agents
    agents = [
        Agent(grid[1][1], grid[ROWS-2][ROWS-2], AGENT_COLORS[0], "Agent-Blue"),
        Agent(grid[ROWS-2][1], grid[1][ROWS-2], AGENT_COLORS[1], "Agent-Purple"),
        Agent(grid[ROWS//2][1], grid[ROWS//2][ROWS-2], AGENT_COLORS[2], "Agent-Orange")
    ]
    
    # Initial Pathing
    for agent in agents:
        agent.path = a_star(grid, agent.current_node, agent.end_node)
        add_log(f"[{agent.name_id}] A* Path calculated successfully.")
        
    # Start Telemetry Thread
    add_log("Starting Telemetry Broadcast to Web Dashboard...")
    threading.Thread(target=send_telemetry_loop, args=(agents,), daemon=True).start()

    clock = pygame.time.Clock()
    run = True
    
    while run:
        draw_background(win)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Compute next positions to avoid agent-to-agent collisions
        occupied_nodes = [a.current_node for a in agents if a.current_node != a.end_node]
        
        for agent in agents:
            # Draw Path
            if agent.current_node != agent.end_node and agent.path and len(agent.path) > 0:
                points = [(n.x + GRID_SIZE//2, n.y + GRID_SIZE//2) for n in [agent.current_node] + agent.path[agent.path_index:]]
                if len(points) >= 2:
                    pygame.draw.lines(win, agent.color, False, points, 2)
                    
            # Draw Goal Marker
            pygame.draw.rect(win, agent.color, (agent.end_node.x + 2, agent.end_node.y + 2, GRID_SIZE - 4, GRID_SIZE - 4), 2, border_radius=4)

            if agent.current_node == agent.end_node:
                agent.status = "Destination Reached!"
                agent.target_speed = 0
                agent.distance = 200
                continue
                
            if agent.path and agent.path_index < len(agent.path):
                next_step = agent.path[agent.path_index]
                
                # Direction vector
                dx = next_step.col - agent.current_node.col
                dy = next_step.row - agent.current_node.row
                if dx != 0 or dy != 0:
                    agent.robot_dir = (dx, dy)
                    
                # Yield to other agents
                if next_step in occupied_nodes and next_step != agent.current_node:
                    agent.target_speed = 0
                    agent.status = "Yielding to traffic"
                    agent.distance = 15
                    if random.random() < 0.05:
                        add_log(f"[{agent.name_id}] Rerouting around traffic...")
                        agent.path = a_star(grid, agent.current_node, agent.end_node)
                        agent.path_index = 0
                
                # Dynamic Pedestrian Alert
                elif random.random() < 0.005 and next_step != agent.end_node: 
                    next_step.make_obstacle("pedestrian", dynamic=True)
                    agent.status = "DYNAMIC ALERT! PEDESTRIAN"
                    agent.target_speed = 0
                    agent.distance = 5
                    add_log(f"[{agent.name_id}] EMERGENCY BRAKE: Pedestrian Detected!")
                    
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    agent.path = a_star(grid, agent.current_node, agent.end_node)
                    agent.path_index = 0
                
                else:
                    agent.target_speed = 45
                    agent.distance = random.randint(120, 200)
                    if next_step.is_obstacle:
                        agent.status = "Path blocked. Rerouting..."
                        for row in grid:
                            for node in row:
                                node.update_neighbors(grid)
                        agent.path = a_star(grid, agent.current_node, agent.end_node)
                        agent.path_index = 0
                    else:
                        agent.status = "Cruising"
                        agent.current_node = next_step
                        agent.path_index += 1
                        
            # Update currently occupied nodes for the next agent check
            occupied_nodes = [a.current_node for a in agents if a.current_node != a.end_node]
            
        # Draw Overlays
        for row in grid:
            for spot in row:
                if spot.is_obstacle:
                    spot.draw(win)

        for agent in agents:
            draw_top_down_car(win, agent.current_node.x, agent.current_node.y, agent.color, agent.robot_dir)

        # HUD
        hud = pygame.Surface((WIDTH, 80))
        hud.set_alpha(220)
        hud.fill((10, 10, 10))
        win.blit(hud, (0, HEIGHT - 80))
        
        for i, agent in enumerate(agents):
            color = (231, 76, 60) if "ALERT" in agent.status or "Yield" in agent.status else agent.color
            text = font.render(f"[{agent.name_id}]: {agent.status}", True, color)
            win.blit(text, (20, HEIGHT - 75 + (i * 20)))
        
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
