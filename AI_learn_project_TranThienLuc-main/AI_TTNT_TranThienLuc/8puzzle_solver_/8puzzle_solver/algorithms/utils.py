# Tap hop cac ham tien ich dung chung phuc vu tinh toan logic cho he thong

# Cau hinh trang thai dich (Goal state) mac dinh: 0 la vi tri trong
GOAL = [1, 2, 3, 4, 5, 6, 7, 8, 0]  

def is_goal(state, goal):
    return state == goal

def get_blank_pos(state):
    return state.index(0)

def get_neighbors(state):
    valid_successors = []
    blank_index = get_blank_pos(state)
    r_coord, c_coord = blank_index // 3, blank_index % 3

    directional_offsets = []
    if r_coord > 0: directional_offsets.append(-3)  # Dich chuyen LEN
    if r_coord < 2: directional_offsets.append(3)   # Dich chuyen XUONG
    if c_coord > 0: directional_offsets.append(-1)  # Dich chuyen SANG TRAI
    if c_coord < 2: directional_offsets.append(1)   # Dich chuyen SANG PHAI

    for offset in directional_offsets:
        cloned_state = state[:]
        target_swap_idx = blank_index + offset
        
        # Thao tac hoan doi vi tri o trong voi o so ben canh
        cloned_state[blank_index], cloned_state[target_swap_idx] = cloned_state[target_swap_idx], cloned_state[blank_index]
        valid_successors.append(cloned_state)

    return valid_successors

def heuristic(state, goal):
    # Su dung thuoc do Khoang cach Manhattan de do luong do sai lech
    total_manhattan_dist = 0
    for current_idx, cell_value in enumerate(state):
        if cell_value != 0:
            correct_goal_idx = goal.index(cell_value)
            
            # Tinh toan khoang cach sai biet toa do theo hang va cot
            row_diff = abs(current_idx // 3 - correct_goal_idx // 3)
            col_diff = abs(current_idx % 3 - correct_goal_idx % 3)
            total_manhattan_dist += row_diff + col_diff
            
    return total_manhattan_dist

def is_solvable(state):
    # Thuat toan dem so cap nghich the de xet tinh kha thi cua ma tran luoi
    state_without_blank = [num for num in state if num != 0]
    inversion_pairs_count = 0
    total_elements = len(state_without_blank)
    
    for outer_idx in range(total_elements):
        for inner_idx in range(outer_idx + 1, total_elements):
            if state_without_blank[outer_idx] > state_without_blank[inner_idx]:
                inversion_pairs_count += 1
                
    # Ma tran 8-puzzle co loi giai khi va chi khi tong so cap nghich the la mot so chan
    return (inversion_pairs_count % 2 == 0)