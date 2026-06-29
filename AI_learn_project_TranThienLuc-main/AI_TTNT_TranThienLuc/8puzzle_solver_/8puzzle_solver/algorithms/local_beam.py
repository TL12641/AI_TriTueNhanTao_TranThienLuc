import random
from .utils import get_neighbors, is_goal, heuristic

# Giai thuat Tim kiem Chum Cuc bo (Local Beam Search)
# Thay vi chi giu mot trang thai duy nhat giong nhu Hill Climbing, 
# thuat toan nay duy tri dong thoi 'k' trang thai tot nhat o moi buoc lap.
# Tat ca cac loi di ke can cua ca 'k' trang thai nay se duoc gop chung lai,
# sau do chon ra 'k' phuong an co ham danh gia h thap nhat cho phien tiep theo.

def local_beam_search(start, goal, k=3, max_iter=1000):
    # Khoi tao tap hop k trang thai khoi dau
    beam_candidates = [start]
    for _ in range(k - 1):
        random_layout = list(range(9))
        random.shuffle(random_layout)
        beam_candidates.append(random_layout)

    # Ghi lai hanh trinh di chuyen dua tren nhanh chinh cua nút start
    path_record = [start]
    nodes_counter = 0

    for _ in range(max_iter):
        merged_successors = []

        # 1. Thu thap tat ca cac nuoc di ke can tu k trang thai hien tai
        for active_candidate in beam_candidates:
            for neighbor in get_neighbors(active_candidate):
                merged_successors.append(neighbor)
            nodes_counter += 1

        # 2. Kiem tra xem da co nhanh nao cham dich hay chua
        for outcome in merged_successors:
            if is_goal(outcome, goal):
                path_record.append(outcome)
                return path_record, nodes_counter

        # 3. Sang loc de giữ lai k ket qua xuat xac nhat theo chi so heuristic
        merged_successors.sort(key=lambda item: heuristic(item, goal))
        beam_candidates = merged_successors[:k]

        if beam_candidates:
            path_record.append(beam_candidates[0])

    return None, nodes_counter