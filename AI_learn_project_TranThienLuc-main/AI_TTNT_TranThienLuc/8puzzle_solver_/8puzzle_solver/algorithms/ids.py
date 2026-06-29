from .utils import get_neighbors, is_goal
from .dls import dls

# Thuat toan Tim kiem Chieu sau Dan (Iterative Deepening Search - IDS)
# Logic: Thuc hien goi lap di lap lai thuat toan DLS (Depth Limited Search)
# voi muc gio han do sau tang dan tu 0 cho den max_depth.
# Huong tiep can nay giup tieu ton it bo nho cua DFS ma van giu duoc tinh toi uu cua BFS.

def ids(start, goal, max_depth=50):
    accumulated_nodes = 0

    for current_limit in range(max_depth + 1):
        path_result, nodes_in_step = dls(start, goal, limit=current_limit)
        accumulated_nodes += nodes_in_step
        
        if path_result is not None:
            return path_result, accumulated_nodes

    return None, accumulated_nodes