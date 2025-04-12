def get_neighbors(position: tuple, player_positions: set) -> list:
    row, col = position
    directions = [(0, 1), (1, 0), (1, -1), (-1, 0), (-1, 1), (0, -1)]
    neighbors = [] 
    for dx, dy in directions:
        new_pos = (row + dx, col + dy)
        if new_pos in player_positions:
            neighbors.append(new_pos)
    return neighbors
def dfs(player_positions: set, player_id: int, size: int) -> bool:
    if not player_positions:
        return False    
    visited = set()
    if player_id == 1: 
        start_positions = {pos for pos in player_positions if pos[1] == 0}  
        target_col = size - 1
        def is_goal(pos):
            return pos[1] == target_col
    else: 
        start_positions = {pos for pos in player_positions if pos[0] == 0}  
        target_row = size - 1
        def is_goal(pos):
            return pos[0] == target_row
    if not start_positions:
        return False
    for start in start_positions:
        if start in visited:
            continue 
        stack = [start]
        visited.add(start)
        while stack:
            current = stack.pop() 
            if is_goal(current):
                return True    
            for neighbor in get_neighbors(current, player_positions):
                if neighbor not in visited:
                    visited.add(neighbor)
                    stack.append(neighbor)
    return False