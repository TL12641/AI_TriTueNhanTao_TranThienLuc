from .utils import get_neighbors, is_goal, heuristic

# Giai thuat leo doi don gian (Simple Hill Climbing)
# Su dung ham heuristic de danh gia trang thai.
# Gia tri cang cao cang tot, o day quy doi bang: gia_tri = -heuristic
# Ngay khi gap mot trang thai lan can dau tien co ket qua tot hon trang thai hien tai,
# thuat toan se lap tuc chuyen sang trang thai do ma khong can quet het cac phuong an con lai.

def simple_hill_climbing(start, goal):
    active_state = start
    trace_path = [active_state]
    expanded_nodes_count = 0

    # Chuyen doi tu tieu chi min-heuristic sang max-value
    active_score = -heuristic(active_state, goal)

    while True:
        possible_moves = get_neighbors(active_state)
        expanded_nodes_count += 1
        has_moved = False

        for next_move in possible_moves:
            score_candidate = -heuristic(next_move, goal)

            # Chi can tim thay phuong an dau tien phat trien hon la chuyen huong ngay
            if score_candidate > active_score:
                active_state = next_move
                active_score = score_candidate
                trace_path.append(active_state)
                has_moved = True
                break  

        # Neu da quet qua ma khong co vi tri nao tot hon thi ngat vong lap (dat cuc dai cuc bo)
        if not has_moved:
            break

    if is_goal(active_state, goal):
        return trace_path, expanded_nodes_count
    return None, expanded_nodes_count