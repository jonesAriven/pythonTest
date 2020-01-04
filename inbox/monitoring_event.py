import sys
import time
import logging
from watchdog.observers import Observer  # pip install watchdog
from watchdog.events import FileSystemEventHandler
from pyCache import SearchCache
import traceback

class MyLoggingEventHandler(FileSystemEventHandler):
    """Logs all the events captured."""
    searchCache = SearchCache()
    def on_moved(self, event):
        super(MyLoggingEventHandler, self).on_moved(event)

        what = 'directory' if event.is_directory else 'file'
        src_path = event.src_path.replace("\\","/")
        dest_path =  event.dest_path.replace("\\","/")
        logging.info("Moved %s: from %s to %s", what, src_path,
                     dest_path)
        if src_path.find("~$") == -1 and src_path.find(".tmp") == -1 and dest_path.find("~$") == -1 and dest_path.find(".tmp") == -1 and src_path.find(".TMP") == -1 :
            self.searchCache.update_chche_1("Moved",what,src_path, dest_path)

    def on_created(self, event):
        super(MyLoggingEventHandler, self).on_created(event)

        what = 'directory' if event.is_directory else 'file'
        src_path = event.src_path.replace("\\","/")
        logging.info("Created %s: %s", what, src_path)
        if src_path.find("~$") == -1 and src_path.find(".tmp") == -1 and src_path.find(".TMP") == -1 :
            self.searchCache.update_chche_1("Created",what,src_path)

    def on_deleted(self, event):
        super(MyLoggingEventHandler, self).on_deleted(event)

        what = 'directory' if event.is_directory else 'file'
        src_path = event.src_path.replace("\\","/")
        logging.info("Deleted %s: %s", what, src_path)
        if src_path.find("~$") == -1 and src_path.find(".tmp") == -1 and src_path.find(".TMP") == -1:
            self.searchCache.update_chche_1("Deleted",what,src_path)

    def on_modified(self, event):
        super(MyLoggingEventHandler, self).on_modified(event)

        what = 'directory' if event.is_directory else 'file'
        src_path = event.src_path.replace("\\","/")
        logging.info("Modified %s: %s", what, src_path)
        if src_path.find("~$") == -1 and src_path.find(".tmp") == -1 and src_path.find(".TMP") == -1:
            if src_path  == "E:/jonesWorkSpace/windowTimerTask/pythontool/search/console.log":
                pass
            else:
                self.searchCache.update_chche_1("Modified",what,src_path)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    # path = sys.argv[1] if len(sys.argv) > 1 else '.'
    path = "E:/java/ideaWorkspace/pythonTest/tmp"
    event_handler = MyLoggingEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        traceback.print_exc()
    observer.join()



