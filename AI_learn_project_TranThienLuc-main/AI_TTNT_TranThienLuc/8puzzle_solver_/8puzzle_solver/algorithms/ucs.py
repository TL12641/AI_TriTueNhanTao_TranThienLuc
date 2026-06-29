import heapq
from .utils import get_neighbors, is_goal

# Thuat toan Tim kiem Chi phi Dong nhat (Uniform Cost Search - UCS)
# Dung hang doi uu tien (Priority Queue) dua tren tong chi phi tich luy g(n) de duyet.
# Vi chi phi di chuyen giua moi o la nhu nhau (= 1), phuong phap nay dat hieu qua
# tuong tu nhu BFS mo rong nhung co logic quan ly gia tri chinh xac hon.

def ucs(start, goal):
    if is_goal(start, goal):
        return [start], 0

    unique_id = 0
    # Cau truc luu trong heap: (accumulated_cost, id, current_state, history_path)
    pq_frontier = [(0, unique_id, start, [start])]
    heapq.heapify(pq_frontier)

    closed_explored_set = set()
    expanded_nodes = 0

    while pq_frontier:
        current_g, _, active_node, trace_path = heapq.heappop(pq_frontier)
        node_signature = tuple(active_node)
        
        if node_signature in closed_explored_set:
            continue
            
        closed_explored_set.add(node_signature)
        expanded_nodes += 1

        if is_goal(active_node, goal):
            return trace_path, expanded_nodes

        for child in get_neighbors(active_node):
            child_key = tuple(child)
            if child_key not in closed_explored_set:
                updated_g = current_g + 1  # Chi phi di chuyen dong nhat la 1 buoc
                unique_id += 1
                heapq.heappush(pq_frontier, (updated_g, unique_id, child, trace_path + [child]))

    return None, expanded_nodes