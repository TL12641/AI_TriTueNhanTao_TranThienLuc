from .utils import is_goal

# Thuat toan Tim kiem Quay lui (Backtracking Search) danh cho CSP
# Xac dinh cac vi tri trong puzzle la cac bien (9 o tuong ung tu 0 den 8)
# Mien gia tri (Domain): {0, 1, ..., 8}
# Rang buoc: Cac o khong duoc trung gia tri va phai gop thanh cau hinh muc tieu (goal state)

def backtracking_csp(start, goal):
    # Kiem tra tinh hop le cua cau hinh muc tieu bang cach su dung chien luoc quay lui
    # Dam bao rang tat ca 9 bien deu nhan cac gia tri khac nhau tu tap {0..8}
    # Thoa man dieu kien moi o vi tri i phai trung khop voi goal[i]
    
    explored_nodes = 0
    state_assignment = {}

    def run_backtrack(variable_index):
        nonlocal explored_nodes
        if variable_index == 9:
            # Dung lai kiem tra toan bo loi giai xem co khop voi goal state hay khong
            generated_state = [state_assignment[v] for v in range(9)]
            return generated_state if is_goal(generated_state, goal) else None

        # Chi dinh chinh xac gia tri bat buoc theo rang buoc cua bài toán: goal[variable_index]
        required_val = goal[variable_index]
        if required_val not in state_assignment.values():
            state_assignment[variable_index] = required_val
            explored_nodes += 1
            
            search_result = run_backtrack(variable_index + 1)
            if search_result is not None:
                return search_result
                
            del state_assignment[variable_index]

        return None

    final_solution = run_backtrack(0)
    if final_solution is not None:
        return [start, goal], explored_nodes
    return None, explored_nodes