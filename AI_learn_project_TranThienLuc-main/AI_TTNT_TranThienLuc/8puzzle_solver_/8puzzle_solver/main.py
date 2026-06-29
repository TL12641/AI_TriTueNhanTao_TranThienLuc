import tkinter as tk
from tkinter import ttk, messagebox
import random
import threading
import time

# Giữ nguyên phần import từ module hệ thống của bạn
from algorithms import (bfs, dfs, dls, ids, ucs, greedy, astar, idastar,
                        simple_hill_climbing, stochastic_hill_climbing,
                        random_restart_hill_climbing, local_beam_search,
                        simulated_annealing, and_or_search, sensorless_search,
                        minimax, alpha_beta, expectimax,
                        backtracking_csp, forward_checking, ac3,
                        is_solvable, GOAL)

TARGET_STATE = GOAL

# ── BẢNG MÀU MỚI (Style Nord / Charcoal Modern) ──────────────────────
THEME_BG       = "#2e3440"  # Xám nền chính
THEME_PANEL    = "#232831"  # Xám tối cho panel
COLOR_TILE     = "#88c0d0"  # Xanh ngọc cho các ô số
COLOR_TILE_TXT = "#2e3440"  # Chữ trên ô số
COLOR_EMPTY    = "#3b4252"  # Ô trống
COLOR_SUCCESS  = "#a3be8c"  # Xanh lá cây dịu
COLOR_ALERT    = "#bf616a"  # Đỏ nhạt cảnh báo
COLOR_SUBTITLE = "#d8dee9"  # Chữ phụ
COLOR_MAIN_TXT = "#e5e9f0"  # Chữ chính
COLOR_SPECIAL  = "#b48ead"  # Tím pastel cho tiêu đề
COLOR_BTN_ON   = "#81a1c1"  # Nút khi kích hoạt
COLOR_BTN_OFF  = "#434c5e"  # Nút mặc định
COLOR_LINE     = "#4c566a"  # Đường viền

FONT_FAMILY = "Consolas"

# ── PHÂN NHÓM CÁC GIẢI THUẬT ─────────────────────────────────────────
ALGORITHM_REGISTRY = [
    ("Uninformed Search", [
        ("BFS", "Breadth-First Search"),
        ("DFS", "Depth-First Search"),
        ("DLS", "Depth-Limited Search"),
        ("IDS", "Iterative Deepening"),
        ("UCS", "Uniform Cost Search"),
    ]),
    ("Informed Search", [
        ("Greedy", "Greedy Best-First"),
        ("A*", "A* Search"),
        ("IDA*", "Iterative Deepening A*"),
    ]),
    ("Local Search", [
        ("Hill Climbing", "Simple Hill Climbing"),
        ("Stochastic HC", "Stochastic HC"),
        ("Random Restart HC", "Random Restart HC"),
        ("Local Beam", "Local Beam Search"),
        ("Simulated Annealing", "Simulated Annealing"),
    ]),
    ("Non-deterministic", [
        ("AND-OR Search", "AND-OR Search"),
        ("Sensorless Search", "Sensorless / Belief State"),
    ]),
    ("Adversarial Search", [
        ("Minimax", "Minimax Search"),
        ("Alpha-Beta", "Alpha-Beta Pruning"),
        ("Expectimax", "Expectimax Search"),
    ]),
    ("Constraint Satisfaction", [
        ("Backtracking CSP", "Backtracking Search"),
        ("Forward Checking", "Forward Checking"),
        ("AC-3", "Arc Consistency AC-3"),
    ]),
]


class PuzzleSolverGUI:
    def __init__(self, main_window):
        self.window = main_window
        self.window.title("Dashboard - 8 Puzzle Solver")
        self.window.configure(bg=THEME_BG)
        self.window.resizable(True, True)

        # Cấu hình hiển thị tràn màn hình
        screen_w = self.window.winfo_screenwidth()
        screen_h = self.window.winfo_screenheight()
        self.window.geometry(f"{screen_w}x{screen_h}+0+0")
        self.window.state("zoomed")

        # Quản lý trạng thái dữ liệu
        self.grid_state = [1, 2, 3, 4, 5, 0, 7, 8, 6]
        self.path_solution = []
        self.step_pointer = 0
        self.is_playing = False
        
        # Biến điều khiển Tkinter
        self.limit_dls_val = tk.IntVar(value=20)
        self.beam_k_val = tk.IntVar(value=3)
        self.selected_algo = tk.StringVar(value="BFS")
        self.delay_speed = tk.DoubleVar(value=0.4)

        self.initialize_layout()
        self.render_puzzle_grid()

    def initialize_layout(self):
        """Khởi tạo bố cục các cột giao diện (Đã đảo thứ tự cột so với gốc)"""
        # Cột 1: Chọn thuật toán (Chuyển sang bên trái ngoài cùng)
        panel_algo = tk.Frame(self.window, bg=THEME_PANEL, padx=15, pady=15)
        panel_algo.pack(side=tk.LEFT, fill=tk.Y)

        # Cột 2: Bàn cờ hiển thị (Nằm ở giữa)
        panel_board = tk.Frame(self.window, bg=THEME_BG, padx=20, pady=15)
        panel_board.pack(side=tk.LEFT, fill=tk.Y)

        # Cột 3: Nhật ký chạy (Nằm bên phải ngoài cùng)
        panel_history = tk.Frame(self.window, bg=THEME_PANEL, padx=15, pady=15)
        panel_history.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.setup_algo_panel(panel_algo)
        self.setup_board_panel(panel_board)
        self.setup_history_panel(panel_history)

    def setup_board_panel(self, container):
        """Thiết kế khu vực hiển thị bàn cờ và các nút chức năng chính"""
        tk.Label(container, text="8-PUZZLE SYSTEM",
                 font=(FONT_FAMILY, 15, "bold"),
                 bg=THEME_BG, fg=COLOR_SPECIAL).pack(pady=(0, 10))

        # Canvas vẽ ô số
        self.board_canvas = tk.Canvas(container, width=285, height=285,
                                      bg=THEME_PANEL, highlightthickness=1,
                                      highlightbackground=COLOR_LINE)
        self.board_canvas.pack()

        # Khu vực lệnh Trộn/Đặt lại
        action_row = tk.Frame(container, bg=THEME_BG)
        action_row.pack(fill=tk.X, pady=(10, 5))

        self.create_custom_btn(action_row, "⚡ Shuffle", self.execute_shuffle, COLOR_BTN_ON, COLOR_TILE_TXT, is_bold=True).pack(side=tk.LEFT, padx=(0, 5), fill=tk.X, expand=True)
        self.create_custom_btn(action_row, "🧹 Reset", self.execute_reset, COLOR_BTN_OFF, COLOR_MAIN_TXT).pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Nút kích hoạt tìm kiếm
        self.trigger_btn = tk.Button(container, text="🔥 START SOLVER",
                                     command=self.launch_solver,
                                     bg=COLOR_SUCCESS, fg=COLOR_TILE_TXT,
                                     font=(FONT_FAMILY, 11, "bold"),
                                     relief=tk.FLAT, pady=7, cursor="hand2")
        self.trigger_btn.pack(fill=tk.X, pady=(10, 5))

        # Đường gạch ngang phân cách
        divider = tk.Frame(container, bg=COLOR_LINE, height=1)
        divider.pack(fill=tk.X, pady=8)

        # Điều hướng tiến trình kết quả
        self.lbl_step_counter = tk.StringVar(value="Progress: -- / --")
        tk.Label(container, textvariable=self.lbl_step_counter,
                 font=(FONT_FAMILY, 9), bg=THEME_BG, fg=COLOR_SUBTITLE).pack(anchor=tk.W)

        nav_row = tk.Frame(container, bg=THEME_BG)
        nav_row.pack(fill=tk.X, pady=5)
        self.create_custom_btn(nav_row, "◀ Prev", self.step_backward, COLOR_BTN_OFF, COLOR_MAIN_TXT).pack(side=tk.LEFT, padx=(0, 4), fill=tk.X, expand=True)
        self.create_custom_btn(nav_row, "Next ▶", self.step_forward, COLOR_BTN_OFF, COLOR_MAIN_TXT).pack(side=tk.LEFT, padx=(0, 4), fill=tk.X, expand=True)
        self.create_custom_btn(nav_row, "⏩ Auto", self.run_autoplay, COLOR_BTN_OFF, COLOR_MAIN_TXT).pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Thanh trượt tốc độ giải
        speed_row = tk.Frame(container, bg=THEME_BG)
        speed_row.pack(fill=tk.X, pady=(5, 5))
        tk.Label(speed_row, text="Interval:", font=(FONT_FAMILY, 9),
                 bg=THEME_BG, fg=COLOR_SUBTITLE).pack(side=tk.LEFT)
        tk.Scale(speed_row, from_=0.05, to=1.5, resolution=0.05,
                 orient=tk.HORIZONTAL, variable=self.delay_speed,
                 bg=THEME_BG, fg=COLOR_MAIN_TXT, highlightthickness=0,
                 troughcolor=COLOR_BTN_OFF, length=180,
                 showvalue=False).pack(side=tk.LEFT, padx=5)

        # Khung chứa thông số tùy biến động theo thuật toán
        self.dynamic_param_area = tk.Frame(container, bg=THEME_BG)
        self.dynamic_param_area.pack(fill=tk.X, pady=(5, 0))

        # Dòng trạng thái hệ thống bên dưới cùng
        self.txt_status_bar = tk.StringVar(value="Hệ thống sẵn sàng. Chọn thuật toán.")
        tk.Label(container, textvariable=self.txt_status_bar,
                 font=(FONT_FAMILY, 8), bg=THEME_BG, fg=COLOR_SUBTITLE,
                 wraplength=280, justify=tk.LEFT).pack(anchor=tk.W, pady=(8, 0))

    def setup_algo_panel(self, container):
        """Tạo danh sách cây chọn thuật toán bằng Radiobutton"""
        tk.Label(container, text="Select Algorithm", font=(FONT_FAMILY, 12, "bold"),
                 bg=THEME_PANEL, fg=COLOR_SPECIAL).pack(anchor=tk.W, pady=(0, 5))

        self.selected_algo.trace_add("write", lambda *_: self.handle_algo_selection_change())

        workspace_canvas = tk.Canvas(container, bg=THEME_PANEL, highlightthickness=0)
        scroller = tk.Scrollbar(container, orient=tk.VERTICAL, command=workspace_canvas.yview)
        scrollable_container = tk.Frame(workspace_canvas, bg=THEME_PANEL)

        scrollable_container.bind("<Configure>", lambda e: workspace_canvas.configure(scrollregion=workspace_canvas.bbox("all")))
        workspace_canvas.create_window((0, 0), window=scrollable_container, anchor="nw")
        workspace_canvas.configure(yscrollcommand=scroller.set)

        workspace_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroller.pack(side=tk.RIGHT, fill=tk.Y)

        for category, list_algos in ALGORITHM_REGISTRY:
            tk.Label(scrollable_container, text=category.upper(),
                     font=(FONT_FAMILY, 8, "bold"),
                     bg=THEME_PANEL, fg=COLOR_SUBTITLE).pack(anchor=tk.W, pady=(8, 2))

            tk.Frame(scrollable_container, bg=COLOR_LINE, height=1).pack(fill=tk.X, pady=(0, 4))

            for code, detail in list_algos:
                item_row = tk.Frame(scrollable_container, bg=THEME_PANEL)
                item_row.pack(fill=tk.X, pady=1)

                r_btn = tk.Radiobutton(item_row, variable=self.selected_algo, value=code,
                                       text=code, font=(FONT_FAMILY, 10, "bold"),
                                       bg=THEME_PANEL, fg=COLOR_MAIN_TXT,
                                       activebackground=THEME_PANEL, activeforeground=COLOR_SPECIAL,
                                       selectcolor=THEME_PANEL, indicatoron=True,
                                       cursor="hand2", relief=tk.FLAT)
                r_btn.pack(side=tk.LEFT)

                tk.Label(item_row, text=f" - {detail}", font=(FONT_FAMILY, 8),
                         bg=THEME_PANEL, fg=COLOR_SUBTITLE).pack(side=tk.LEFT)

        def handle_mouse_scroll(evt):
            workspace_canvas.yview_scroll(int(-1 * (evt.delta / 120)), "units")
        workspace_canvas.bind_all("<MouseWheel>", handle_mouse_scroll)

    def setup_history_panel(self, container):
        """Thiết kế khung log hiển thị kết quả"""
        top_row = tk.Frame(container, bg=THEME_PANEL)
        top_row.pack(fill=tk.X, pady=(0, 5))

        tk.Label(top_row, text="Execution Trace Log", font=(FONT_FAMILY, 12, "bold"),
                 bg=THEME_PANEL, fg=COLOR_SPECIAL).pack(side=tk.LEFT)

        self.create_custom_btn(top_row, "Wipe Logs", self.clear_execution_logs, COLOR_BTN_OFF, COLOR_SUBTITLE, font_size=8).pack(side=tk.RIGHT)

        self.txt_summary_metrics = tk.StringVar(value="")
        tk.Label(container, textvariable=self.txt_summary_metrics,
                 font=(FONT_FAMILY, 9), bg=THEME_PANEL, fg=COLOR_SUCCESS,
                 anchor=tk.W, justify=tk.LEFT).pack(fill=tk.X, pady=(0, 5))

        text_wrapper = tk.Frame(container, bg=THEME_PANEL)
        text_wrapper.pack(fill=tk.BOTH, expand=True)

        v_scroll = tk.Scrollbar(text_wrapper)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.console_output = tk.Text(text_wrapper, width=30, font=(FONT_FAMILY, 9),
                                      bg=COLOR_EMPTY, fg=COLOR_MAIN_TXT,
                                      yscrollcommand=v_scroll.set, relief=tk.FLAT,
                                      state=tk.DISABLED, spacing1=2, padx=6, pady=6)
        self.console_output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scroll.config(command=self.console_output.yview)

        # Định nghĩa thẻ màu cho text log
        self.console_output.tag_config("err", foreground=COLOR_ALERT, font=(FONT_FAMILY, 9, "bold"))
        self.console_output.tag_config("ok", foreground=COLOR_SUCCESS, font=(FONT_FAMILY, 9, "bold"))
        self.console_output.tag_config("header", foreground=COLOR_SPECIAL, font=(FONT_FAMILY, 9, "bold"))
        self.console_output.tag_config("muted", foreground=COLOR_SUBTITLE)
        self.console_output.tag_config("step", foreground=COLOR_MAIN_TXT)
        self.console_output.tag_config("cur", background=COLOR_BTN_ON, foreground=COLOR_TILE_TXT)

    def create_custom_btn(self, container, label, action, bg_color, fg_color, is_bold=False, font_size=9):
        weight = "bold" if is_bold else "normal"
        return tk.Button(container, text=label, command=action,
                         bg=bg_color, fg=fg_color,
                         font=(FONT_FAMILY, font_size, weight),
                         relief=tk.FLAT, padx=6, pady=3, cursor="hand2",
                         activebackground=COLOR_SPECIAL, activeforeground=COLOR_TILE_TXT)

    def render_puzzle_grid(self, target_list=None):
        """Vẽ lưới ma trận các ô số lên màn hình"""
        if target_list is None:
            target_list = self.grid_state
        self.board_canvas.delete("all")
        block_size = 88
        gap = 5
        for idx, val in enumerate(target_list):
            row_idx, col_idx = idx // 3, idx % 3
            pos_x1 = col_idx * (block_size + gap) + gap
            pos_y1 = row_idx * (block_size + gap) + gap
            pos_x2, pos_y2 = pos_x1 + block_size, pos_y1 + block_size
            
            if val == 0:
                self.board_canvas.create_rectangle(pos_x1, pos_y1, pos_x2, pos_y2,
                                                   fill=COLOR_EMPTY, outline=COLOR_LINE, width=1)
            else:
                self.board_canvas.create_rectangle(pos_x1, pos_y1, pos_x2, pos_y2,
                                                   fill=COLOR_TILE, outline="", width=0)
                self.board_canvas.create_text((pos_x1 + pos_x2) // 2, (pos_y1 + pos_y2) // 2,
                                              text=str(val), font=(FONT_FAMILY, 26, "bold"),
                                              fill=COLOR_TILE_TXT)

    def write_to_console(self, msg, tag_style="step"):
        self.console_output.config(state=tk.NORMAL)
        self.console_output.insert(tk.END, msg + "\n", tag_style)
        self.console_output.see(tk.END)
        self.console_output.config(state=tk.DISABLED)

    def append_step_snapshot_to_console(self, step_num, current_layout, is_active=False):
        style = "cur" if is_active else "step"
        buffer_lines = [f"Step {step_num}:"]
        for r in range(3):
            sub_row = current_layout[r*3:(r+1)*3]
            buffer_lines.append("  " + " ".join(str(item) if item != 0 else "·" for item in sub_row))
        self.console_output.config(state=tk.NORMAL)
        self.console_output.insert(tk.END, "\n".join(buffer_lines) + "\n", style)
        self.console_output.see(tk.END)
        self.console_output.config(state=tk.DISABLED)

    def clear_execution_logs(self):
        self.console_output.config(state=tk.NORMAL)
        self.console_output.delete("1.0", tk.END)
        self.console_output.config(state=tk.DISABLED)
        self.txt_summary_metrics.set("")

    def handle_algo_selection_change(self):
        """Xử lý thay đổi widget tùy biến khi chọn thuật toán đặc biệt"""
        for child in self.dynamic_param_area.winfo_children():
            child.destroy()

        current_selection = self.selected_algo.get()
        if current_selection == "DLS":
            tk.Label(self.dynamic_param_area, text="Limit Depth:",
                     font=(FONT_FAMILY, 9), bg=THEME_BG, fg=COLOR_SUBTITLE).pack(side=tk.LEFT)
            tk.Spinbox(self.dynamic_param_area, from_=1, to=50,
                       textvariable=self.limit_dls_val, width=5,
                       font=(FONT_FAMILY, 9), bg=COLOR_BTN_OFF, fg=COLOR_MAIN_TXT,
                       buttonbackground=COLOR_BTN_OFF, relief=tk.FLAT).pack(side=tk.LEFT, padx=5)

        elif current_selection == "Local Beam":
            tk.Label(self.dynamic_param_area, text="Beam Size (k):",
                     font=(FONT_FAMILY, 9), bg=THEME_BG, fg=COLOR_SUBTITLE).pack(side=tk.LEFT)
            tk.Spinbox(self.dynamic_param_area, from_=1, to=20,
                       textvariable=self.beam_k_val, width=5,
                       font=(FONT_FAMILY, 9), bg=COLOR_BTN_OFF, fg=COLOR_MAIN_TXT,
                       buttonbackground=COLOR_BTN_OFF, relief=tk.FLAT).pack(side=tk.LEFT, padx=5)

    def execute_shuffle(self):
        while True:
            temp_list = list(range(9))
            random.shuffle(temp_list)
            if is_solvable(temp_list):
                break
        self.grid_state = temp_list
        self.path_solution = []
        self.step_pointer = 0
        self.txt_summary_metrics.set("")
        self.lbl_step_counter.set("Progress: -- / --")
        self.txt_status_bar.set("Đã xáo trộn ngẫu nhiên. Bấm START SOLVER.")
        self.render_puzzle_grid()

    def execute_reset(self):
        self.grid_state = [1, 2, 3, 4, 5, 0, 7, 8, 6]
        self.path_solution = []
        self.step_pointer = 0
        self.txt_summary_metrics.set("")
        self.lbl_step_counter.set("Progress: -- / --")
        self.txt_status_bar.set("Đã khôi phục trạng thái mặc định.")
        self.render_puzzle_grid()
        self.clear_execution_logs()

    def launch_solver(self):
        algo_mode = self.selected_algo.get()
        initial_state = self.grid_state[:]
        target_goal = TARGET_STATE

        ignored_solvability_checks = ["Backtracking CSP", "Forward Checking", "AC-3"]
        if algo_mode not in ignored_solvability_checks and not is_solvable(initial_state):
            messagebox.showerror("Thông báo lỗi", "Vị trí khởi tạo này không có giải pháp khả thi!")
            return

        self.clear_execution_logs()
        self.write_to_console(f">> Khởi động thuật toán: {algo_mode}...", "muted")
        self.txt_status_bar.set(f"Đang tính toán giải pháp [{algo_mode}]...")
        self.trigger_btn.config(state=tk.DISABLED, text="⏳ Processing...")

        def core_search_process():
            start_timestamp = time.time()
            
            # Cấu trúc rẽ nhánh thực thi thuật toán
            if algo_mode == "BFS":
                out_path, node_count = bfs(initial_state, target_goal)
            elif algo_mode == "DFS":
                out_path, node_count = dfs(initial_state, target_goal)
            elif algo_mode == "DLS":
                out_path, node_count = dls(initial_state, target_goal, limit=self.limit_dls_val.get())
            elif algo_mode == "IDS":
                out_path, node_count = ids(initial_state, target_goal)
            elif algo_mode == "UCS":
                out_path, node_count = ucs(initial_state, target_goal)
            elif algo_mode == "Greedy":
                out_path, node_count = greedy(initial_state, target_goal)
            elif algo_mode == "A*":
                out_path, node_count = astar(initial_state, target_goal)
            elif algo_mode == "IDA*":
                out_path, node_count = idastar(initial_state, target_goal)
            elif algo_mode == "Hill Climbing":
                out_path, node_count = simple_hill_climbing(initial_state, target_goal)
            elif algo_mode == "Stochastic HC":
                out_path, node_count = stochastic_hill_climbing(initial_state, target_goal)
            elif algo_mode == "Random Restart HC":
                out_path, node_count = random_restart_hill_climbing(initial_state, target_goal)
            elif algo_mode == "Local Beam":
                out_path, node_count = local_beam_search(initial_state, target_goal, k=self.beam_k_val.get())
            elif algo_mode == "Simulated Annealing":
                out_path, node_count = simulated_annealing(initial_state, target_goal)
            elif algo_mode == "AND-OR Search":
                out_path, node_count = and_or_search(initial_state, target_goal)
            elif algo_mode == "Sensorless Search":
                out_path, node_count = sensorless_search(initial_state, target_goal)
            elif algo_mode == "Minimax":
                out_path, node_count = minimax(initial_state, target_goal)
            elif algo_mode == "Alpha-Beta":
                out_path, node_count = alpha_beta(initial_state, target_goal)
            elif algo_mode == "Expectimax":
                out_path, node_count = expectimax(initial_state, target_goal)
            elif algo_mode == "Backtracking CSP":
                out_path, node_count = backtracking_csp(initial_state, target_goal)
            elif algo_mode == "Forward Checking":
                out_path, node_count = forward_checking(initial_state, target_goal)
            elif algo_mode == "AC-3":
                out_path, node_count = ac3(initial_state, target_goal)
            else:
                out_path, node_count = None, 0
                
            execution_duration = time.time() - start_timestamp
            self.window.after(0, lambda: self.finalize_search_results(out_path, node_count, execution_duration, algo_mode))

        threading.Thread(target=core_search_process, daemon=True).start()

    def finalize_search_results(self, path, nodes, duration, method_used):
        self.trigger_btn.config(state=tk.NORMAL, text="🔥 START SOLVER")

        if path is None:
            self.txt_status_bar.set("Thất bại: Không tìm thấy đường đi.")
            self.txt_summary_metrics.set(f"✗ {method_used} | {nodes} nodes | {duration:.3f}s")
            self.write_to_console(f"✗ Tìm kiếm thất bại.", "err")
            self.write_to_console(f"  Nodes explored: {nodes}", "muted")
            return

        self.path_solution = path
        self.step_pointer = 0
        total_steps = len(path) - 1

        self.txt_status_bar.set(f"Hoàn thành: {total_steps} bước | {nodes} nodes")
        self.txt_summary_metrics.set(f"✓ {method_used} | {total_steps} steps | {nodes} nodes | {duration:.3f}s")
        self.lbl_step_counter.set(f"Progress: 0 / {total_steps}")

        self.write_to_console(f"✓ Hoàn tất giải thuật: {method_used}", "ok")
        self.write_to_console(f"  Tổng số bước : {total_steps}", "muted")
        self.write_to_console(f"  Thời gian     : {duration:.4f} giây", "muted")
        self.write_to_console("═" * 30, "muted")
        
        for index, matrix in enumerate(self.path_solution):
            self.append_step_snapshot_to_console(index, matrix, is_active=(index == 0))

        self.render_puzzle_grid(self.path_solution[0])

    def sync_board_with_pointer(self):
        self.lbl_step_counter.set(f"Progress: {self.step_pointer} / {len(self.path_solution) - 1}")
        self.render_puzzle_grid(self.path_solution[self.step_pointer])

    def step_forward(self):
        if not self.path_solution or self.step_pointer >= len(self.path_solution) - 1:
            return
        self.step_pointer += 1
        self.sync_board_with_pointer()

    def step_backward(self):
        if not self.path_solution or self.step_pointer <= 0:
            return
        self.step_pointer -= 1
        self.sync_board_with_pointer()

    def run_autoplay(self):
        if not self.path_solution or self.is_playing:
            return
        self.is_playing = True

        def automatic_worker():
            limit = len(self.path_solution) - 1
            while self.step_pointer < limit and self.is_playing:
                self.step_pointer += 1
                current_frame = self.path_solution[self.step_pointer]
                self.window.after(0, lambda f=current_frame: self.render_puzzle_grid(f))
                self.window.after(0, lambda: self.lbl_step_counter.set(f"Progress: {self.step_pointer} / {limit}"))
                time.sleep(self.delay_speed.get())
            self.is_playing = False

        threading.Thread(target=automatic_worker, daemon=True).start()


if __name__ == "__main__":
    main_frame = tk.Tk()
    application = PuzzleSolverGUI(main_frame)
    main_frame.mainloop()