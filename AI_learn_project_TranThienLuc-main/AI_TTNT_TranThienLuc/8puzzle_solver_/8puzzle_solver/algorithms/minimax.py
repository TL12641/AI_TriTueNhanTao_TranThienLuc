from .utils import get_neighbors, is_goal, heuristic

# Thuat toan Tim kiem Minimax gia dinh trong bai toan 8-puzzle
# Do khong co doi thu doi khang thuc te, mo hinh thuc hien gia lap:
# - Nut MAX: Đai dien cho Agent, tim kiem cac nuoc di lam giam diem heuristic.
# - Nut MIN: Gia lap doi thu ao, co tinh lua chon cac nuoc di lam tang mieu ta rui ro (tang h).
# He thong dan xen giua hai muc nay de dua ra lua chon an toan ve mat tong the.

MAX_DEPTH = 6

def _run_minimax_calculation(state, target_goal, depth, maximizer_flag, route_path, closed_set):
    if is_goal(state, target_goal):
        return route_path[:], heuristic(state, target_goal), 1
    if depth == 0:
        return None, heuristic(state, target_goal), 1

    state_signature = tuple(state)
    if state_signature in closed_set:
        return None, heuristic(state, target_goal), 0
    closed_set = closed_set | {state_signature}

    available_neighbors = get_neighbors(state)
    examined_nodes = 1
    optimal_route = None

    if maximizer_flag:
        worst_score = float('inf')  # MAX huong den viec toi thieu hoa gia tri h
        for next_step in available_neighbors:
            route_path.append(next_step)
            sub_path, calculated_h, counter = _run_minimax_calculation(next_step, target_goal, depth - 1, False, route_path, closed_set)
            examined_nodes += counter
            
            if calculated_h < worst_score:
                worst_score = calculated_h
                optimal_route = sub_path if sub_path else route_path[:]
            route_path.pop()
    else:
        worst_score = float('-inf')  # MIN huong den viec toi da hoa gia tri h
        for next_step in available_neighbors:
            route_path.append(next_step)
            sub_path, calculated_h, counter = _run_minimax_calculation(next_step, target_goal, depth - 1, True, route_path, closed_set)
            examined_nodes += counter
            
            if calculated_h > worst_score:
                worst_score = calculated_h
                optimal_route = sub_path
            route_path.pop()

    return optimal_route, worst_score, examined_nodes


def minimax(start, goal):
    final_path = [start[:]]
    current_state = start[:]
    total_nodes_visited = 0
    global_closed_list = set()

    for _ in range(100):
        if is_goal(current_state, goal):
            return final_path, total_nodes_visited

        global_closed_list.add(tuple(current_state))
        moves = get_neighbors(current_state)

        optimum_value = float('inf')
        selected_move = None
        current_layer_nodes = 0

        for move in moves:
            _, score, steps = _run_minimax_calculation(move, goal, MAX_DEPTH - 1, False, [move], global_closed_list)
            current_layer_nodes += steps
            if score < optimum_value:
                optimum_value = score
                selected_move = move

        total_nodes_visited += current_layer_nodes

        if selected_move is None:
            break

        current_state = selected_move[:]
        final_path.append(current_state)

    if is_goal(current_state, goal):
        return final_path, total_nodes_visited
    return None, total_nodes_visited