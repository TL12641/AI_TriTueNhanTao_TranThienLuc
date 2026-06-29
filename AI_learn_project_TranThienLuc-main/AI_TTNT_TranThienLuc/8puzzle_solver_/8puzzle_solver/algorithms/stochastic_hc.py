import random
from .utils import get_neighbors, is_goal, heuristic

# Chien luoc Leo doi xac suat (Stochastic Hill Climbing)
# Logic phat trien:
# 1. Quet toan bo danh sach cac o ke can cua vi tri hien tai.
# 2. Sang loc ra tap hop cac nuoc di thuc su mang lai gia tri tich cuc (h_next < h_current).
# 3. Thay vi chon ngay phuong an tot nhat, thuat toan lua chon NGAU NHIEN mot trong so chung.
# Huong di nay tao ra tinh bat ngo va giup giai thuat khong bi rap khuon.

def stochastic_hill_climbing(start, goal, max_iter=10000):
    active_layout = start
    journey_path = [active_layout]
    nodes_expanded_count = 0

    for _ in range(max_iter):
        if is_goal(active_layout, goal):
            return journey_path, nodes_expanded_count

        surrounding_nodes = get_neighbors(active_layout)
        nodes_expanded_count += 1

        base_metric = -heuristic(active_layout, goal)

        # Gom nhom tat ca cac phuong an co loi vao danh sach cho
        promising_pool = [node for node in surrounding_nodes 
                          if -heuristic(node, goal) > base_metric]

        if not promising_pool:
            # Khong con huong phat trien nao tot hon, dung lai (dat cuc dai dia phuong)
            break
        else:
            # Rut tham ngau nhien lay mot nuoc di trong pool
            selected_node = random.choice(promising_pool)
            active_layout = selected_node
            journey_path.append(active_layout)

    return journey_path, nodes_expanded_count