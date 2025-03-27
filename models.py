from dataclasses import dataclass, field
from typing import Dict

@dataclass
class ProcessInfo:
    pid: int
    name: str
    memory: int  # в байтах
    cpu_percent: float
    exe_path: str = ""

@dataclass
class TaskMngrInfo:
    processes: Dict[int, ProcessInfo] = field(default_factory=dict)
