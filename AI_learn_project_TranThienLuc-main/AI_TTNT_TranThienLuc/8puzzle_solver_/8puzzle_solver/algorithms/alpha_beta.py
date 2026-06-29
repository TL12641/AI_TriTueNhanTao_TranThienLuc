from .utils import get_neighbors, is_goal, heuristic

# Chien luoc cat tia Alpha-Beta giup tang toc thuat toan Minimax
# Quy tac cat nhanh:
# - Tai node MAX: dung xet neu alpha vuot qua hoac bang beta
# - Tai node MIN: dung xet neu beta nho hon hoac bang alpha
# Tiet kiem thoi gian duyet cay ma van dam bao tim thay ket qua tuong duong.

LIMIT_DEPTH = 6

def _evaluate_alpha_beta(current_state, target_goal, current_depth, maximizer_turn, val_alpha, val_beta, current_path, closed_set):
    if is_goal(current_state, target_goal):
        return current_path[:], heuristic(current_state, target_goal), 1
    if current_depth == 0:
        return None, heuristic(current_state, target_goal), 1

    state_key = tuple(current_state)
    if state_key in closed_set:
        return None, heuristic(current_state, target_goal), 0
    closed_set = closed_set | {state_key}

    possible_moves = get_neighbors(current_state)
    examined_nodes = 1
    optimal_path = None

    if maximizer_turn:
        inf_score = float('inf')
        for next_move in possible_moves:
            current_path.append(next_move)
            res_path, res_score, count = _evaluate_alpha_beta(next_move, target_goal, current_depth - 1, False, val_alpha, val_beta, current_path, closed_set)
            examined_nodes += count
            
            if res_score < inf_score:
                inf_score = res_score
                optimal_path = res_path if res_path else current_path[:]
            val_beta = min(val_beta, inf_score)
            current_path.pop()
            
            if val_beta <= val_alpha:  # Thuc hien cat tia nhanh tai node MAX
                break
    else:
        inf_score = float('-inf')
        for next_move in possible_moves:
            current_path.append(next_move)
            res_path, res_score, count = _evaluate_alpha_beta(next_move, target_goal, current_depth - 1, True, val_alpha, val_beta, current_path, closed_set)
            examined_nodes += count
            
            if res_score > inf_score:
                inf_score = res_score
                optimal_path = res_path
            val_alpha = max(val_alpha, inf_score)
            current_path.pop()
            
            if val_beta <= val_alpha:  # Thuc hien cat tia nhanh tai node MIN
                break

    return optimal_path, inf_score, examined_nodes


def alpha_beta(start, goal):
    trace_path = [start[:]]
    state_pointer = start[:]
    nodes_counter = 0
    global_visited = set()

    for _ in range(100):
        if is_goal(state_pointer, goal):
            return trace_path, nodes_counter

        global_visited.add(tuple(state_pointer))
        valid_neighbors = get_neighbors(state_pointer)

        min_heuristic_score = float('inf')
        selected_move = None
        current_batch_nodes = 0

        for move in valid_neighbors:
            _, computed_score, step_num = _evaluate_alpha_beta(move, goal, LIMIT_DEPTH - 1, False,
                                                              float('-inf'), float('inf'), [move], global_visited)
            current_batch_nodes += step_num
            if computed_score < min_heuristic_score:
                min_heuristic_score = computed_score
                selected_move = move

        nodes_counter += current_batch_nodes

        if selected_move is None:
            break

        state_pointer = selected_move[:]
        trace_path.append(state_pointer)

    if is_goal(state_pointer, goal):
        return trace_path, nodes_counter
    return None, nodes_counter