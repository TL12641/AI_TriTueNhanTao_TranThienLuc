from .utils import is_goal

# Thuat toan Forward Checking trong bai toan thoa man rang buoc (CSP)
# Logic: Ngay sau khi xep gia tri cho bien nay, tien hanh loai tru luon gia tri do
# khoi danh sach mien gia tri hop le cua cac bien tiep theo chua duoc gan.
# Neu xuat hien mien gia tri rong -> Gặp be tac, lap tuc quay lui (backtrack).

def forward_checking(start, goal):
    nodes_count = 0
    current_assignment = {}

    def run_fc_backtrack(var_index, valid_pool):
        nonlocal nodes_count
        if var_index == 9:
            evaluated_state = [current_assignment[v] for v in range(9)]
            return evaluated_state if is_goal(evaluated_state, goal) else None

        target_val = goal[var_index]

        # Kiem tra som (Forward check): neu gia tri can thiet da bi loai khoi pool
        if target_val not in valid_pool:
            return None  

        current_assignment[var_index] = target_val
        nodes_count += 1

        # Rut gon mien gia tri cho cac bien ke tiep
        updated_pool = [item for item in valid_pool if item != target_val]

        # Kiem tra dead-end dua tren so bien con sot lai
        unassigned_count = 9 - var_index - 1
        if len(updated_pool) >= unassigned_count:
            search_res = run_fc_backtrack(var_index + 1, updated_pool)
            if search_res is not None:
                return search_res

        del current_assignment[var_index]
        return None

    full_values = list(range(9))
    final_res = run_fc_backtrack(0, full_values)

    if final_res is not None:
        return [start, goal], nodes_count
    return None, nodes_count