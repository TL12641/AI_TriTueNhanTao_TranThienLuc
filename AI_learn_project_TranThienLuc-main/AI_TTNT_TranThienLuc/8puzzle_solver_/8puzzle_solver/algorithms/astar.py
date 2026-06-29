import heapq
from .utils import get_neighbors, is_goal, heuristic

# Giai thuat tim kiem dinh huong A* (A-Star Search)
# Logic thu hien:
# 1. Nap phan tu dau tien vao FRONTIER, tinh f(Start) = g(Start) + h(Start)
# 2. Tao danh sach REACHED luu cac trang thai da kiem duyet
# 3. Lap den khi rong tập FRONTIER:
#    a. Lay ra nut co gia tri f thap nhat
#    b. Neu dat den GOAL thi hoan tat va tra ve ket qua
#    c. Chuyen nut dang xet sang tap REACHED
#    d. Quét tat ca cac dinh ke m cua nut hien tai:
#       i.  g_new(m) = g(node) + cost_step (mac dinh bang 1)
#       ii. Neu m nam trong tap REACHED:
#           - Chi xet tiep khi chi phi moi tot hon (g_new < g cu), xoa khoi REACHED de cap nhat lai
#       iii.Neu m dang co trong FRONTIER va g_new < g cu: cap nhat lai chi phi f va dinh cha
#       iv. Truong hop m hoan toan moi: khoi tao gia tri, tinh f(m) va day vao FRONTIER

def astar(start, goal):
    init_h = heuristic(start, goal)
    init_g = 0
    init_f = init_g + init_h

    unique_id = 0
    # Du lieu luu dang: (f_value, id, g_value, current_state, full_path)
    search_frontier = [(init_f, unique_id, init_g, start, [start])]
    heapq.heapify(search_frontier)

    visited_reached = {}         
    frontier_lookup = {}    
    frontier_lookup[tuple(start)] = init_g

    total_expanded = 0

    while search_frontier:
        f_val, _, g_val, current_node, path_trace = heapq.heappop(search_frontier)
        node_key = tuple(current_node)

        # Tranh xu ly lai cac ban ghi loi thoi da duoc cap nhat truoc do
        if node_key in frontier_lookup and frontier_lookup[node_key] < g_val:
            continue
        if node_key in visited_reached and visited_reached[node_key] < g_val:
            continue

        if is_goal(current_node, goal):
            return path_trace, total_expanded

        if node_key in frontier_lookup:
            del frontier_lookup[node_key]
            
        visited_reached[node_key] = g_val
        total_expanded += 1

        for neighbor_node in get_neighbors(current_node):
            neighbor_key = tuple(neighbor_node)
            calculated_g = g_val + 1  

            if neighbor_key in visited_reached:
                if calculated_g >= visited_reached[neighbor_key]:
                    continue
                del visited_reached[neighbor_key]

            if neighbor_key in frontier_lookup:
                if calculated_g < frontier_lookup[neighbor_key]:
                    frontier_lookup[neighbor_key] = calculated_g
                    m_heuristic = heuristic(neighbor_node, goal)
                    m_f_score = calculated_g + m_heuristic
                    unique_id += 1
                    heapq.heappush(search_frontier, (m_f_score, unique_id, calculated_g, neighbor_node, path_trace + [neighbor_node]))
            else:
                m_heuristic = heuristic(neighbor_node, goal)
                m_f_score = calculated_g + m_heuristic
                frontier_lookup[neighbor_key] = calculated_g
                unique_id += 1
                heapq.heappush(search_frontier, (m_f_score, unique_id, calculated_g, neighbor_node, path_trace + [neighbor_node]))

    return None, total_expanded