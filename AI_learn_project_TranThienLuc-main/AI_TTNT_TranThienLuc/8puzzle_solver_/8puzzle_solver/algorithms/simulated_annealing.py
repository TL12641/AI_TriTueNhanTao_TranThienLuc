import math
import random
from .utils import get_neighbors, is_goal, heuristic

# Giai thuat Luyen kim gia lap (Simulated Annealing)
# Dua tren nguyen ly vat ly:
# - Khi nhiet do T con cao: Chap nhan di vao cac nuoc di te (tang rui ro h) de thoat khoi be tac cuc bo.
# - Khi nhiet do T ha thap: Siết chat dieu kien, chi uu tien cac nuoc tot (giam h) de hoi tu ve dich.

def simulated_annealing(start, goal, T_max=1000.0, T_min=0.01, alpha=0.995, max_iter=100000):
    active_node = start[:]
    history_trace = [active_node[:]]
    visited_records = {tuple(active_node)}
    total_steps = 0
    temperature = T_max

    for _ in range(max_iter):
        if is_goal(active_node, goal):
            return history_trace, total_steps
        if temperature < T_min:
            break

        adjacent_options = get_neighbors(active_node)
        total_steps += 1
        random_candidate = random.choice(adjacent_options)

        # energy_diff > 0 co nghia la random_candidate giup giam thieu sai so heuristic (tot hon)
        energy_diff = heuristic(active_node, goal) - heuristic(random_candidate, goal)

        if energy_diff > 0:
            is_accepted = True
        else:
            # Tinh toan xac suat thong ke de chap nhan nuoc di xau
            is_accepted = random.random() < math.exp(energy_diff / temperature)

        if is_accepted:
            active_node = random_candidate[:]
            node_key = tuple(active_node)
            if node_key not in visited_records:
                history_trace.append(active_node[:])
                visited_records.add(node_key)

        # Ha nhiet dan theo ty le alpha
        temperature *= alpha

    if is_goal(active_node, goal):
        return history_trace, total_steps
    return None, total_steps