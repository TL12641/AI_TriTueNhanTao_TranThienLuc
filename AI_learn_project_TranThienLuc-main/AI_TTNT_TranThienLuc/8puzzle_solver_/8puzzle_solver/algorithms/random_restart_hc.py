import random
from .utils import get_neighbors, is_goal, heuristic, is_solvable

# Thuat toan Leo doi Khoi dong Ngau nhien (Random Restart Hill Climbing)
# Day la bien the giup khac phuc nhuoc diem ket tai cac vung cuc dai cuc bo cua Hill Climbing.
# Neu thuat toan roi vao vi tri be tac ma chua dat den Goal, he thong se tu dong
# xao tron ngau nhien mot trang thai moi (dam bao trang thai do co loi giai) de bat dau lai tu dau.

def random_restart_hill_climbing(start, goal, max_restart=50):
    expanded_nodes = 0
    journey_path = [start]

    for attempt_idx in range(max_restart):
        # Tran dau tien chay tu vi tri xuất phat, cac tran sau sinh layout ngau nhien
        if attempt_idx == 0:
            active_layout = start
        else:
            while True:
                shuffled_state = list(range(9))
                random.shuffle(shuffled_state)
                if is_solvable(shuffled_state):
                    break
            active_layout = shuffled_state
            journey_path.append(active_layout)  # Nap vi tri khoi dong lai vao path de lam dau

        while True:
            if is_goal(active_layout, goal):
                journey_path.append(active_layout)
                return journey_path, expanded_nodes

            valid_moves = get_neighbors(active_layout)
            expanded_nodes += 1

            current_metric = -heuristic(active_layout, goal)

            # Loc ra toan bo cac vi tri lan can mang lai ket qua tot hon
            favorable_moves = [move for move in valid_moves 
                               if -heuristic(move, goal) > current_metric]

            if not favorable_moves:
                # Roi vao ngoc cut, ngat vong lap phu nay de kich hoat phien restart tiep theo
                break
            else:
                # Chon ra phuong an uu viet nhat tu nhom loi di co loi
                best_move = min(favorable_moves, key=lambda layout: heuristic(layout, goal))
                active_layout = best_move
                journey_path.append(active_layout)

    return None, expanded_nodes