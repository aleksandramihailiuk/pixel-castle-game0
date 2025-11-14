import random
import os
import time

# Профессиональные ASCII символы для визуализации
PIXEL = {
    'wall': '▓▓', 
    'path': '  ', 
    'player': '☻ ', 
    'exit': '▓▓', 
    'treasure': '$ ', 
    'trap': 'X ', 
    'health': '♥ '
}

def play_sound(sound_type):
    """Воспроизведение звуковых эффектов"""
    if sound_type == "treasure":
        print("[ЗВУК МОНЕТЫ]")
    elif sound_type == "trap":
        print("[ЗВУК ЛОВУШКИ]")
    elif sound_type == "win":
        print("[ПОБЕДНАЯ МЕЛОДИЯ]")
    elif sound_type == "move":
        print("[ШАГИ]")
    elif sound_type == "wall":
        print("[УДАР О СТЕНУ]")
    time.sleep(0.3)

def clear_screen():
    """Очистка экрана"""
    os.system('cls' if os.name == 'nt' else 'clear')

def show_title():
    """Показ профессионального заголовка"""
    clear_screen()
    print("=" * 50)
    print("           ПИКСЕЛЬНЫЙ ЗАМОК")
    print("         Игра-лабиринт с сокровищами")
    print("=" * 50)
    print()
    print("          Исследуйте подземелья!")
    print("      Собирайте сокровища, избегайте ловушек")
    print("          Найдите путь к свободе!")
    print()

def find_connected_areas(maze, start_x, start_y):
    """Находит все клетки, достижимые из стартовой позиции"""
    visited = set()
    queue = [(start_x, start_y)]
    accessible_cells = []
    
    while queue:
        x, y = queue.pop(0)
        if (x, y) in visited:
            continue
            
        visited.add((x, y))
        if maze[y][x] == PIXEL['path']:
            accessible_cells.append((x, y))
        
        # Проверяем всех соседей
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (0 <= nx < len(maze[0]) and 0 <= ny < len(maze) and 
                maze[ny][nx] != PIXEL['wall'] and (nx, ny) not in visited):
                queue.append((nx, ny))
    
    return accessible_cells

def create_maze(level):
    """Создание случайного лабиринта"""
    # Размер лабиринта увеличивается с уровнем
    base_size = 15
    size_increase = min(level // 3, 5)
    width = base_size + size_increase
    height = 10 + size_increase
    
    maze = [[PIXEL['wall'] for _ in range(width)] for _ in range(height)]
    
    # Плотность стен: растет с уровнем, но не более 50%
    wall_density = min(0.25 + (level * 0.02), 0.5)
    
    # Создаем основные проходы
    for i in range(1, height-1):
        for j in range(1, width-1):
            if random.random() > wall_density:
                maze[i][j] = PIXEL['path']
    
    # Гарантируем путь от старта до финиша
    for i in range(1, height-1):
        maze[i][1] = PIXEL['path']
        maze[i][width-2] = PIXEL['path']
    
    for j in range(1, width-1):
        maze[1][j] = PIXEL['path']
        maze[height-2][j] = PIXEL['path']
    
    # Устанавливаем игрока и выход (выход выглядит как стена но другого типа)
    maze[1][1] = PIXEL['player']
    maze[height-2][width-2] = '[]'  # Выход выглядит как дверь
    
    # Находим ВСЕ доступные клетки из стартовой позиции
    all_accessible_cells = find_connected_areas(maze, 1, 1)
    
    # Убираем стартовую позицию и выход из списка доступных для размещения предметов
    available_positions = [pos for pos in all_accessible_cells 
                          if pos != (1, 1) and pos != (width-2, height-2)]
    
    # Размещаем сокровища (только в доступных местах!)
    treasure_count = 0
    treasures_needed = min(5 + level, len(available_positions) - 3)
    
    if available_positions and treasures_needed > 0:
        # Берем случайные позиции из доступных
        treasure_positions = random.sample(available_positions, min(treasures_needed, len(available_positions)))
        for x, y in treasure_positions:
            maze[y][x] = PIXEL['treasure']
            treasure_count += 1
            # Убираем эту позицию из доступных для ловушек
            available_positions.remove((x, y))
    
    # Размещаем ловушки (только в доступных местах!)
    trap_count = 0
    traps_to_place = min(3 + level, len(available_positions))
    
    if available_positions and traps_to_place > 0:
        trap_positions = random.sample(available_positions, min(traps_to_place, len(available_positions)))
        for x, y in trap_positions:
            maze[y][x] = PIXEL['trap']
            trap_count += 1
    
    return maze, treasures_needed, width, height

def find_player(maze):
    """Поиск позиции игрока в лабиринте"""
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            if maze[y][x] == PIXEL['player']:
                return x, y
    return None

def display_game(maze, treasures_found, treasures_needed, health, moves, level):
    """Отображение игрового интерфейса"""
    clear_screen()
    
    print("=" * 50)
    print(f"          ПИКСЕЛЬНЫЙ ЗАМОК - Уровень {level}")
    print("=" * 50)
    print(f" Сокровища: {treasures_found}/{treasures_needed} | Здоровье: {health}/100")
    print(f" Ходы: {moves} | Сложность: {'*' * min(level, 5)}")
    print("-" * 50)
    
    # Отображение лабиринта с рамкой
    print("+" + "-" * (len(maze[0]) * 2) + "+")
    for row in maze:
        print("|", end="")
        for cell in row:
            print(cell, end="")
        print("|")
    print("+" + "-" * (len(maze[0]) * 2) + "+")
    
    print("-" * 50)
    print(" Управление: W,A,S,D - движение (можно несколько)")
    print("            R - рестарт, Q - выход")
    print("=" * 50)
    print(" Обозначения: ☻ - вы, $ - сокровище, X - ловушка")
    print("             [] - выход, ▓▓ - стены")

def process_movement_sequence(maze, move_sequence, treasures_found, treasures_needed, health, moves, level):
    """Обработка последовательности движений"""
    player_x, player_y = find_player(maze)
    
    for move in move_sequence:
        new_x, new_y = player_x, player_y
        
        if move == 'W': new_y -= 1
        elif move == 'S': new_y += 1
        elif move == 'A': new_x -= 1
        elif move == 'D': new_x += 1
        else:
            continue
        
        # Проверка возможности хода
        if (0 <= new_x < len(maze[0]) and 0 <= new_y < len(maze) and 
            maze[new_y][new_x] != PIXEL['wall']):
            
            moves += 1
            target_cell = maze[new_y][new_x]
            
            if target_cell == PIXEL['treasure']:
                treasures_found += 1
                print(f">>> Найдено сокровище! ({treasures_found}/{treasures_needed})")
                play_sound("treasure")
                
            elif target_cell == PIXEL['trap']:
                health -= 15
                print(f">>> Ловушка! -15 здоровья. Осталось: {health}")
                play_sound("trap")
                if health <= 0:
                    break
                
            elif target_cell == '[]':  # Выход
                if treasures_found < treasures_needed:
                    print(f">>> Нужно собрать все сокровища! Осталось: {treasures_needed - treasures_found}")
                    break
                else:
                    # Игрок дошел до выхода
                    maze[player_y][player_x] = PIXEL['path']
                    maze[new_y][new_x] = PIXEL['player']
                    player_x, player_y = new_x, new_y
                    break
            
            # Перемещение игрока
            maze[player_y][player_x] = PIXEL['path']
            maze[new_y][new_x] = PIXEL['player']
            player_x, player_y = new_x, new_y
            
            play_sound("move")
            
        else:
            # Удар о стену
            health -= 5
            print(f">>> Удар о стену! -5 здоровья. Осталось: {health}")
            play_sound("wall")
            if health <= 0:
                break
            else:
                break
    
    return treasures_found, health, moves

def main_game():
    """Основная игровая функция"""
    level = 1
    games_played = 0
    total_score = 0
    
    show_title()
    
    while True:
        maze, treasures_needed, width, height = create_maze(level)
        treasures_found = 0
        health = 100
        moves = 0
        
        print(f"\n>>> Игра #{games_played + 1} - Уровень {level}")
        print(f">>> Размер карты: {width}x{height}")
        print(">>> Задание: Соберите все сокровища и найдите выход")
        print(">>> Опасности: Ловушки (-15 HP), Стены (-5 HP)")
        print(">>> Можно вводить несколько команд подряд (например: DDDRR)")
        input(">>> Нажмите Enter для начала...")
        
        game_active = True
        while game_active:
            display_game(maze, treasures_found, treasures_needed, health, moves, level)
            
            # Проверка условий победы
            player_x, player_y = find_player(maze)
            if (player_x == width-2 and player_y == height-2 and 
                treasures_found >= treasures_needed):
                display_game(maze, treasures_found, treasures_needed, health, moves, level)
                score = (health * 10) + (100 - moves) + (level * 50)
                total_score += score
                print(f"\n*** ПОБЕДА! Уровень {level} пройден! ***")
                print(f"*** Награда: {score} очков ***")
                print(f"*** Здоровье: {health} | Ходы: {moves} | Уровень: {level} ***")
                print(f"*** Общий счет: {total_score} очков ***")
                play_sound("win")
                level += 1
                games_played += 1
                input("\n>>> Нажмите Enter для продолжения...")
                break
            
            # Проверка проигрыша
            if health <= 0:
                display_game(maze, treasures_found, treasures_needed, health, moves, level)
                print(f"\n*** ПОРАЖЕНИЕ! Вы погибли на уровне {level}! ***")
                print(f"*** Игр сыграно: {games_played} ***")
                print(f"*** Общий счет: {total_score} очков ***")
                play_sound("trap")
                print("\n>>> Начинаем новую игру...")
                level = 1
                games_played += 1
                time.sleep(3)
                break
            
            # Обработка ввода
            move_input = input("\n>>> Ваш ход (W/A/S/D/Q/R): ").upper().strip()
            
            if move_input == 'Q':
                print(f"\n*** Выход из игры. Ваш счет: {total_score} очков ***")
                return
            elif move_input == 'R':
                print("\n>>> Рестарт игры...")
                time.sleep(1)
                break
            
            # Обработка последовательности движений
            if move_input:
                treasures_found, health, moves = process_movement_sequence(
                    maze, move_input, treasures_found, treasures_needed, health, moves, level
                )

# Запуск игры
if __name__ == "__main__":
    main_game()
