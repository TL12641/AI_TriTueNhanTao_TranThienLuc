from collections import deque
from .utils import get_neighbors, is_goal

# Thuat toan duyet do thi theo chieu rong (BFS)
# Su dung hang doi FIFO de luu cac nut o bien (frontier)
# Su dung mot tap hop de luu giu cac trang thai da qua (visited)

def bfs(start, goal):
    initial_node = start
    if is_goal(initial_node, goal):
        return [initial_node], 0

    # Lua chon hang doi de dam bao dung co che FIFO
    search_queue = deque()
    search_queue.append((initial_node, [initial_node]))

    visited_states = set()
    visited_states.add(tuple(initial_node))

    total_expanded = 0

    while search_queue:
        current_node, current_path = search_queue.popleft()
        total_expanded += 1

        for successor in get_neighbors(current_node):
            successor_key = tuple(successor)
            if is_goal(successor, goal):
                return current_path + [successor], total_expanded
            
            # Kiem tra xem trang thai ke tiep da tung duoc xet qua hay chua
            in_queue = any(tuple(item[0]) == successor_key for item in search_queue)
            if (successor_key not in visited_states) and (not in_queue):
                visited_states.add(successor_key)
                search_queue.append((successor, current_path + [successor]))

    return None, total_expanded