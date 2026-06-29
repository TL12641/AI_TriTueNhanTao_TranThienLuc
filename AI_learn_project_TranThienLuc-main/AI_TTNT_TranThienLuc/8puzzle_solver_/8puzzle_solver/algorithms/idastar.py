from .utils import get_neighbors, is_goal, heuristic

# Thuật toán IDA* (Iterative Deepening A*)
# Su dung co che duyet cay DFS ket hop voi gioi han chi phi f = g + h.
# Sau moi luot duyet, neu chua tim thay ket qua, nguong gioi han (threshold)
# se duoc tang len bang muc chi phi nho nhat tung bi cat o phien truoc đo.

def idastar(start, goal):
    limit_threshold = heuristic(start, goal)
    current_path = [start]
    grand_total_nodes = 0

    while True:
        solution, next_threshold, steps = _perform_dfs_search(current_path, 0, limit_threshold, goal)
        grand_total_nodes += steps

        if solution is not None:
            return solution, grand_total_nodes
        if next_threshold == float('inf'):
            return None, grand_total_nodes

        # Nang muc gioi han len de mo rong pham vi tim kiem o phien tiep theo
        limit_threshold = next_threshold


def _perform_dfs_search(path_stack, g_cost, threshold_bound, destination):
    active_node = path_stack[-1]
    f_cost = g_cost + heuristic(active_node, destination)
    nodes_count = 0

    if f_cost > threshold_bound:
        return None, f_cost, nodes_count  

    if is_goal(active_node, destination):
        return list(path_stack), threshold_bound, nodes_count

    lowest_cutoff_val = float('inf')
    nodes_count += 1

    for child_node in get_neighbors(active_node):
        # Tranh truong hop di vong quanh bang cach kiem tra lich su duong di dang xet
        if tuple(child_node) not in [tuple(node) for node in path_stack]:
            path_stack.append(child_node)
            search_res, temp_threshold, additional_steps = _perform_dfs_search(path_stack, g_cost + 1, threshold_bound, destination)
            nodes_count += additional_steps

            if search_res is not None:
                return search_res, threshold_bound, nodes_count
            
            lowest_cutoff_val = min(lowest_cutoff_val, temp_threshold)
            path_stack.pop()

    return None, lowest_cutoff_val, nodes_count