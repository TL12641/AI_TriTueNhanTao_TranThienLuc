import random
from .utils import get_neighbors, is_goal, heuristic

# Chien luoc tim kiem AND-OR trong moi truong ngau nhien (non-deterministic)
# Gia dinh moi hanh dong co xac suat rui ro lam lech huong sang trang thai khac.
# - Node OR: Nguoi choi chu dong lua chon phuong an toi uu.
# - Node AND: Tat ca moi tinh huong phat sinh bat ngo deu phai co huong giai quyet.

TIMEOUT_DEPTH = 40

def _execute_or_search(current_state, goal_state, tracking_set, depth_level):
    if is_goal(current_state, goal_state):
        return [current_state[:]], 1
    if depth_level > TIMEOUT_DEPTH or tuple(current_state) in tracking_set:
        return None, 0

    tracking_set = tracking_set | {tuple(current_state)}
    total_nodes = 1

    adjacent_states = get_neighbors(current_state)
    adjacent_states.sort(key=lambda s: heuristic(s, goal_state))
    base_h = heuristic(current_state, goal_state)

    for next_step in adjacent_states:
        # Mo phong kha nang "truot" ngau nhien neu tim duoc trang thai thuan loi hon
        possible_outcomes = [next_step]
        accidental_slips = [s for s in adjacent_states if s != next_step and heuristic(s, goal_state) < base_h]
        if accidental_slips:
            possible_outcomes.append(random.choice(accidental_slips))

        sub_plan, step_cost = _execute_and_search(possible_outcomes, goal_state, tracking_set, depth_level + 1)
        total_nodes += step_cost
        if sub_plan is not None:
            return [current_state[:]] + sub_plan, total_nodes

    return None, total_nodes


def _execute_and_search(state_outcomes, goal_state, tracking_set, depth_level):
    if not state_outcomes:
        return [], 0

    total_nodes = 0
    main_plan, step_cost = _execute_or_search(state_outcomes[0], goal_state, tracking_set, depth_level)
    total_nodes += step_cost
    if main_plan is None:
        return None, total_nodes

    # Kiem tra do an toan cho tat ca cac ket qua phu do ngau nhien sinh ra
    for secondary_state in state_outcomes[1:]:
        if not is_goal(secondary_state, goal_state):
            _, backup_cost = _execute_or_search(secondary_state, goal_state, tracking_set, depth_level)
            total_nodes += backup_cost

    return main_plan, total_nodes


def and_or_search(start, goal):
    return _execute_or_search(start[:], goal, set(), 0)