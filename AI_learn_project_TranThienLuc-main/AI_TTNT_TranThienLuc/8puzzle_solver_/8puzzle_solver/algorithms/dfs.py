from .utils import get_neighbors, is_goal

# Thuat toan duyet do thi theo chieu sau (DFS)
# Dung danh sach dang ngan xep LIFO (stack) lam frontier
# Dung tap hop de danh dau cac trang thai da xu ly xong

def dfs(start, goal):
    initial_node = start
    if is_goal(initial_node, goal):
        return [initial_node], 0

    # Khoi tao ngan xep voi cau truc: (state, path)
    nodes_stack = [(initial_node, [initial_node])]

    closed_list = set()
    closed_list.add(tuple(initial_node))

    total_expanded = 0

    while nodes_stack:
        current_node, current_path = nodes_stack.pop()
        total_expanded += 1

        for successor in get_neighbors(current_node):
            successor_key = tuple(successor)
            if is_goal(successor, goal):
                return current_path + [successor], total_expanded
            
            if successor_key not in closed_list:
                closed_list.add(successor_key)
                nodes_stack.append((successor, current_path + [successor]))

    return None, total_expanded