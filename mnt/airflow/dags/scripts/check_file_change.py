import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import sys 
import time
#sys.path.append(os.getcwd()+ '/scripts')
sys.path.insert(0,"..")
#print(sys.path)
from scripts.send_dag_to_controlm import SendDAGtoControlM


last_trigger_time = time.time()

class Watcher:

    def __init__(self, directory=".", handler=FileSystemEventHandler()):
        self.observer = Observer()
        self.handler = handler
        self.directory = directory

    def run(self):
        self.observer.schedule(
            self.handler, self.directory, recursive=True)
        self.observer.start()
        print("\nWatcher Running in {}/\n".format(self.directory))
        try:
            while True:
                time.sleep(1)
        except:
            self.observer.stop()
        self.observer.join()
        print("\nWatcher Terminated\n")


class MyHandler(FileSystemEventHandler):

    def on_modified(self, event):
        
        global last_trigger_time
        current_time = time.time()
        # Your code here
        if event.src_path.find('~') == -1 and (current_time - last_trigger_time) > 1:
            last_trigger_time = current_time
            #filename = event.src_path.split('/')[-1].split('.')[0]
            filename = event.src_path.split('/')[-1]
            if '.py' in filename and 'ctm' in filename:
                filename = filename.split('.')[0]
                print('{} modified and hence updating DAG in Control-M'.format(filename))
                temp = 5
                for i in range(1,1):
                    print('Sleeping for ...', i*5)
                    time.sleep(5)
                print('Done with sleep()..initiating the SendDAGtoControlM')
                SendDAGtoControlM.create_ctm_dag(filename)
    
    def on_created(self, event):
        filename = event.src_path.split('/')[-1]
        if '.py' in filename and 'ctm' in filename:
            filename = filename.split('.')[0]
            print('{} created and hence creating DAG in Control-M'.format(filename)) 

if __name__=="__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    w = Watcher(path, MyHandler())
    w.run()

# Run using below 
# cd dags/scripts
# python check_file_change.py ../main/    