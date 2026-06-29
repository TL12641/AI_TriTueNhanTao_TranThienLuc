from collections import deque
from .utils import is_goal

# Thuat toan AC-3 thiet lap tinh nhat quan cung trong bai toan CSP
# Kiem tra cac cap bien (Xi, Xj): moi gia tri thuoc mien gia tri cua Xi 
# deu phai thoa man it nhat mot gia tri hop le trong mien gia tri cua Xj.
# Ap dung rang buoc: cac bien phai co gia tri khac biet hoan toan.

def _check_and_revise(domain_dict, v_i, v_j):
    has_changed = False
    # Duyet qua ban sao cac gia tri trong mien gia tri cua bien v_i
    for current_val in list(domain_dict[v_i]):
        # Neu khong tim thay gia tri nao khac cua v_j ma khac current_val, ta loai bo no
        if all(other_val == current_val for other_val in domain_dict[v_j]):
            domain_dict[v_i].remove(current_val)
            has_changed = True
    return has_changed


def _execute_ac3(domain_dict, all_vars):
    # Khoi tao hang doi chua cac cap cung phan biet
    arc_queue = deque((x, y) for x in all_vars for y in all_vars if x != y)
    step_count = 0
    
    while arc_queue:
        v_i, v_j = arc_queue.popleft()
        step_count += 1
        
        if _check_and_revise(domain_dict, v_i, v_j):
            if len(domain_dict[v_i]) == 0:
                return False, step_count
            # Them lai cac cung bi anh huong vao hang doi
            for neighbor in all_vars:
                if neighbor != v_j:
                    arc_queue.append((neighbor, v_i))
                    
    return True, step_count


def ac3(start, goal):
    puzzle_vars = list(range(9))
    # Khoi tao mien gia tri ban dau tu 0 den 8 cho ca 9 bien
    current_domains = {var: list(range(9)) for var in puzzle_vars}

    # Giai doan 1: Loc mien gia tri bang AC-3
    is_consistent, total_nodes = _execute_ac3(current_domains, puzzle_vars)
    if not is_consistent:
        return None, total_nodes

    # Giai doan 2: Quay lui tim kiem voi mien gia tri da rut gon
    current_assignment = {}

    def solve_backtrack(idx):
        nonlocal total_nodes
        if idx == 9:
            final_state = [current_assignment[i] for i in range(9)]
            return final_state if is_goal(final_state, goal) else None

        target_value = goal[idx]

        if (target_value in current_domains[idx]) and (target_value not in current_assignment.values()):
            current_assignment[idx] = target_value
            total_nodes += 1

            # Sao chep mien gia tri de chay thu nghiem AC-3 moi
            temp_domains = {key: list(val) for key, val in current_domains.items()}
            temp_domains[idx] = [target_value]
            
            success, additional_nodes = _execute_ac3(temp_domains, puzzle_vars)
            total_nodes += additional_nodes

            if success:
                search_res = solve_backtrack(idx + 1)
                if search_res is not None:
                    return search_res

            del current_assignment[idx]

        return None

    final_res = solve_backtrack(0)
    if final_res is not None:
        return [start, goal], total_nodes
    return None, total_nodes