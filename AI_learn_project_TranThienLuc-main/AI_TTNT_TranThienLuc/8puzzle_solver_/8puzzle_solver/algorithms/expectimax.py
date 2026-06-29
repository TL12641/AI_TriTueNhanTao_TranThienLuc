import random
from .utils import get_neighbors, is_goal, heuristic

# Chien luoc tim kiem cay quyet dinh Expectimax Search
# - Nut MAX: Chon hanh dong giup co ket qua heuristic toi uu nhat.
# - Nut CHANCE: Tinh toan xac suat va lay gia tri trung binh (ky vong toán hoc).
# Ung dung cho mo hinh co cac yeu to rui ro hoac ngau nhien tu moi truong.

MAX_SEARCH_DEPTH = 5

def _calculate_expectimax(state, target, depth, check_max, closed_set):
    if is_goal(state, target):
        return heuristic(state, target), 1
    if depth == 0:
        return heuristic(state, target), 1

    state_key = tuple(state)
    if state_key in closed_set:
        return heuristic(state, target), 0
    closed_set = closed_set | {state_key}

    valid_children = get_neighbors(state)
    examined_count = 1

    if check_max:
        # Xu ly tai nut MAX: chon gia tri chi phi thap nhat
        optimal_score = float('inf')
        for child in valid_children:
            score, count = _calculate_expectimax(child, target, depth - 1, False, closed_set)
            examined_count += count
            optimal_score = min(optimal_score, score)
        return optimal_score, examined_count
    else:
        # Xu ly tai nut CHANCE: Tinh trung binh cong ky vong cua cac nhanh con
        cumulative_score = 0
        for child in valid_children:
            score, count = _calculate_expectimax(child, target, depth - 1, True, closed_set)
            examined_count += count
            cumulative_score += score
        return cumulative_score / len(valid_children), examined_count


def expectimax(start, goal):
    path_trace = [start[:]]
    current_pointer = start[:]
    grand_total_nodes = 0
    history_visited = set()

    for _ in range(100):
        if is_goal(current_pointer, goal):
            return path_trace, grand_total_nodes

        history_visited.add(tuple(current_pointer))
        adjacent_nodes = get_neighbors(current_pointer)

        lowest_cost = float('inf')
        best_candidate = None
        current_batch = 0

        for candidate in adjacent_nodes:
            eval_score, steps = _calculate_expectimax(candidate, goal, MAX_SEARCH_DEPTH - 1, False, history_visited)
            current_batch += steps
            if eval_score < lowest_cost:
                lowest_cost = eval_score
                best_candidate = candidate

        grand_total_nodes += current_batch

        if best_candidate is None:
            break

        current_pointer = best_candidate[:]
        path_trace.append(current_pointer)

    if is_goal(current_pointer, goal):
        return path_trace, grand_total_nodes
    return None, grand_total_nodes