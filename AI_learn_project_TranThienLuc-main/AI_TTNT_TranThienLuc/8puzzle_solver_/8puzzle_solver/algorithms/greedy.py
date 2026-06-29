import heapq
from .utils import get_neighbors, is_goal, heuristic

# Thuat toan Tim kiem Tham lam Best-First Search (Greedy Search)
# Tien trinh hoan thanh:
# 1. Khoi tao tap hop FRONTIER tu nut Start, tinh h(Start) ban dau
# 2. Xay dung tap hop REACHED danh dau cac phuong an da quet qua
# 3. Kiem tra vong lap khi FRONTIER van con phan tu:
#    a. Bop ra nut co gia tri du doan ham h thap nhat trong hang doi priority queue
#    b. Neu nut dang xet thoa man dieu kien dich (Goal) -> Hoan tat thuat toan
#    c. Dua nut nay vao danh sach CLOSED (REACHED) de tranh lap lai, tang dem bien so nut expanded
#    d. Voi moi loi di con m ke can nut hien tai:
#       i. Neu m hoan toan moi (khong co trong FRONTIER lan REACHED) -> Gan quan he va nap vao FRONTIER
#       ii. Cac truong hop khac thi bo qua luon de tiet kiem chi phi

def greedy(start, goal):
    start_h = heuristic(start, goal)

    unique_counter = 0
    # Du lieu luu theo cau truc uu tien: (h_score, counter, state, path)
    priority_frontier = [(start_h, unique_counter, start, [start])]
    heapq.heapify(priority_frontier)

    closed_reached = set()
    total_expanded = 0

    while priority_frontier:
        h_score, _, active_node, history_path = heapq.heappop(priority_frontier)
        active_tuple = tuple(active_node)

        if is_goal(active_node, goal):
            return history_path, total_expanded

        closed_reached.add(active_tuple)
        total_expanded += 1

        # Lay nhanh danh sach cac o dang xet cho trong hang doi
        active_frontier_keys = {tuple(item[2]) for item in priority_frontier}

        for neighbor in get_neighbors(active_node):
            neighbor_key = tuple(neighbor)
            
            # Nut phai hoan toan chua tung xuat hien thi moi duoc vao danh sach xet tiep
            if (neighbor_key not in closed_reached) and (neighbor_key not in active_frontier_keys):
                neighbor_h = heuristic(neighbor, goal)
                unique_counter += 1
                heapq.heappush(priority_frontier, (neighbor_h, unique_counter, neighbor, history_path + [neighbor]))

    return None, total_expanded