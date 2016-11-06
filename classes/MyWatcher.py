# -*- coding: utf-8 -*-
import time
import logging, logging.config
import env_variables
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
logging.config.dictConfig(env_variables.LOGGING)


class Watcher:

    def __init__(self):
        self.observer = Observer()

    def run(self, my_thread):
        """
        this function starts the tread that will play the playlist
        then it launch the watching of stop.p, previous.p and next.p files
        """
        my_thread.start()
        
        # indicate the ba are played
        stop = False
        save_file = os.path.join(env_variables.stopnextprevious_dir, env_variables.stop_file)
        pickle.dump(stop, open( save_file, "wb" ))

        event_handler = Handler(my_thread)
        self.observer.schedule(event_handler, env_variables.stopnextprevious_dir)
        self.observer.start()
        try:
            # watching the files through observer will happen
            # until the player thread has ended its job
            my_thread.join()
            self.observer.stop()
        except Exception:
            self.observer.stop()
            logging.debug("Watcher stopped")
        # wait for the closing of the observer
        self.observer.join()


class Handler(FileSystemEventHandler):

    def __init__(self, my_thread):
        super(Handler, self).__init__()
        self.my_thread = my_thread

    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith(env_variables.next_file):
            self.my_thread.next()

        if not event.is_directory and event.src_path.endswith(env_variables.previous_file):
            self.my_thread.previous()

        if not event.is_directory and event.src_path.endswith(env_variables.stop_file):
            self.my_thread.stop()