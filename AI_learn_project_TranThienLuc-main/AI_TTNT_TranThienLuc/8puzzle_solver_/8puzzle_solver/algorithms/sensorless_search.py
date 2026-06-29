from collections import deque
from .utils import is_goal

# Thuat toan Tim kiem Khong Cam bien (Sensorless Search / Belief State BFS)
# Mo hinh: Agent mu thong tin, khong biet ro minh dang o toa do nao.
# Khai niem 'Belief state': Tap hop chua tat ca cac vi tri ma agent co the dang dung.
# Muc tieu: Tim ra mot chuoi hanh dong duy nhat giup dua moi trang thai trong belief tap trung ve dich.

MAX_BELIEF_SIZE = 6
MAX_NODES = 5000

# Khai bao huong dich chuyen: 0=Len, 1=Xuong, 2=Trai, 3=Phai
SHIFT_STEPS = {0: -3, 1: 3, 2: -1, 3: 1}
BOUNDARY_CHECK = {
    0: lambda r, c: r > 0,
    1: lambda r, c: r < 2,
    2: lambda r, c: c > 0,
    3: lambda r, c: c < 2
}

def _apply_action(belief, action):
    next_belief_pool = set()
    for current_state in belief:
        state_list = list(current_state)
        blank_idx = state_list.index(0)
        row_pos, col_pos = blank_idx // 3, blank_idx % 3
        
        # Neu nuoc di vi pham bien ban co thi loai bo nhanh nay
        if not BOUNDARY_CHECK[action](row_pos, col_pos):
            return None
            
        target_swap = blank_idx + SHIFT_STEPS[action]
        state_list[blank_idx], state_list[target_swap] = state_list[target_swap], state_list[blank_idx]
        next_belief_pool.add(tuple(state_list))
    return frozenset(next_belief_pool)


def _replay(start, actions):
    active_layout = start[:]
    computed_path = [active_layout[:]]
    for act in actions:
        blank_idx = active_layout.index(0)
        target_swap = blank_idx + SHIFT_STEPS[act]
        temp_state = active_layout[:]
        temp_state[blank_idx], temp_state[target_swap] = temp_state[target_swap], temp_state[blank_idx]
        active_layout = temp_state
        computed_path.append(active_layout[:])
    return computed_path


def sensorless_search(start, goal):
    goal_signature = tuple(goal)
    starting_belief = frozenset([tuple(start)])

    search_queue = deque([(starting_belief, [])])
    history_beliefs = {starting_belief}
    expanded_counter = 0

    while search_queue:
        if expanded_counter >= MAX_NODES:
            break

        current_belief, move_history = search_queue.popleft()
        expanded_counter += 1

        # Check xem toan bo moi truong gia dinh trong belief da dong nhat ve dich chua
        if all(single_state == goal_signature for single_state in current_belief):
            return _replay(start, move_history), expanded_counter

        for act_code in range(4):
            computed_belief = _apply_action(current_belief, act_code)
            if computed_belief is None:
                continue
            
            if computed_belief not in history_beliefs:
                history_beliefs.add(computed_belief)
                search_queue.append((computed_belief, move_history + [act_code]))

    return None, expanded_counter