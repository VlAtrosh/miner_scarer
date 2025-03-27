from monitoring import MonitoringSystem
from gui import TaskManagerGUI

def main():
    monitor = MonitoringSystem()
    monitor.start_monitoring()
    
    gui = TaskManagerGUI(monitor)
    gui.mainloop()
    

    monitor.stop_monitoring()

if __name__ == "__main__":
    main()
