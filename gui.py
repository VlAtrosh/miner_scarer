import tkinter as tk
from tkinter import ttk, messagebox
# Исправленный импорт (без точки!)

class TaskManagerGUI(tk.Tk):
    def __init__(self, monitor):
        super().__init__()
        self.monitor = monitor
        self.title("Task Manager")
        self.geometry("1000x600")
        self._create_widgets()
        self._schedule_update()

    def _create_widgets(self):
        self.tree = ttk.Treeview(self, columns=("PID", "Name", "Memory", "CPU", "Path"), show="headings")
        self.tree.heading("PID", text="PID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Memory", text="Memory (MB)")
        self.tree.heading("CPU", text="CPU %")
        self.tree.heading("Path", text="Executable Path")
        self.tree.pack(fill=tk.BOTH, expand=True)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=5)
        self.kill_btn = tk.Button(btn_frame, text="Kill Process", command=self._kill_process)
        self.kill_btn.pack(side=tk.LEFT, padx=5)
        self.info_btn = tk.Button(btn_frame, text="Show Path", command=self._show_path)
        self.info_btn.pack(side=tk.LEFT, padx=5)

    def _schedule_update(self):
        self._update_process_list()
        self.after(1000, self._schedule_update)

    def _update_process_list(self):
        info = self.monitor.get_info()
        self.tree.delete(*self.tree.get_children())
        for pid, proc in info.processes.items():
            self.tree.insert("", "end", values=(
                pid,
                proc.name,
                f"{proc.memory // 1024 // 1024}",
                f"{proc.cpu_percent:.1f}",
                proc.exe_path
            ))

    def _kill_process(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Error", "Select a process")
            return
        pid = int(self.tree.item(selected[0])['values'][0])
        if self.monitor.kill_process(pid):
            self._update_process_list()
        else:
            messagebox.showerror("Error", "Failed to kill process")

    def _show_path(self):
        selected = self.tree.selection()
        if selected:
            path = self.tree.item(selected[0])['values'][4]
            messagebox.showinfo("Path", path)
