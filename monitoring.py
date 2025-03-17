import psutil
import time
from threading import Lock, Thread
from models import TaskMngrInfo, ProcessInfo

class MonitoringSystem:
    def __init__(self):
        self.info = TaskMngrInfo()
        self.lock = Lock()
        self._stop = False

    def update(self) -> TaskMngrInfo:
        new_info = TaskMngrInfo()
        for proc in psutil.process_iter(['pid', 'name', 'memory_info', 'cpu_percent', 'exe']):
            try:
                data = proc.info
                pid = data['pid']
                new_info.processes[pid] = ProcessInfo(
                    pid=pid,
                    name=data['name'] or "Unknown",
                    memory=data['memory_info'].rss if data['memory_info'] else 0,
                    cpu_percent=data['cpu_percent'] or 0.0,
                    exe_path=data['exe'] or ""
                )
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        with self.lock:
            self.info = new_info
        return self.info

    def start_monitoring(self):
        from threading import Thread
        self._stop = False
        self.thread = Thread(target=self._monitoring_loop, daemon=True)
        self.thread.start()

    def _monitoring_loop(self):
        while not self._stop:
            self.update()
            time.sleep(1)

    def stop_monitoring(self):
        self._stop = True

    def get_info(self) -> TaskMngrInfo:
        with self.lock:
            return self.info

    def kill_process(self,pid:int) -> bool:
        try:
            process = psutil.Process(pid)
            process.terminate()
            return True
        except psutil.NoSuchProcess:
            return False
