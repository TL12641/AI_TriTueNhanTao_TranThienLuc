from .utils import get_neighbors, is_goal

# Thuat toan DFS gioi han do sau (Depth Limited Search)
# Neu cay tim kiem dat den nguong cho phep (limit) ma chua thay dich
# se thuc hien ngat nhanh (cutoff) de chuyen sang huong khac

def dls(start, goal, limit=20):
    total_expanded = 0

    def run_dls_recursive(node, history_path, current_limit):
        nonlocal total_expanded
        if is_goal(node, goal):
            return history_path, False  # Dung lai va bao khong ngat (false cutoff)
        if current_limit == 0:
            return None, True   # Chạm nguong gioi han, ngat phuong an nay

        is_cutoff_triggered = False
        total_expanded += 1

        for child in get_neighbors(node):
            # Ngan chan tinh trang lap vong vo tan bang cach check cac nut cha da qua
            if tuple(child) not in [tuple(p) for p in history_path]:
                search_res, cutoff_flag = run_dls_recursive(child, history_path + [child], current_limit - 1)
                
                if cutoff_flag:
                    is_cutoff_triggered = True
                elif search_res is not None:
                    return search_res, False

        if is_cutoff_triggered:
            return None, True
        return None, False

    final_path, _ = run_dls_recursive(start, [start], limit)
    return final_path, total_expanded