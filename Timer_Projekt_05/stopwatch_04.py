import time
import logging
import threading


class Stopwatch:
    def __init__(self, minutes, callback):
        self.minutes = minutes
        self.seconds = minutes * 60
        self.callback = callback
        self._timer_running_lock = threading.Lock()
        self._timer_thread = None
        self._timer_running = False
        self.remaining_minutes=0



    def start(self):
        with self._timer_running_lock:
            self._timer_running = True
            self._timer_thread = threading.Thread(target=self._countdown)
            self._timer_thread.start()
            logging.debug(f"start(): timer_running ist {self._timer_running}")

    def stop(self):
        with self._timer_running_lock:
            self._timer_running = False
            self.stopwatch = None
            self.remaining_minutes=0  
            logging.debug(f"stop():timer_running ist {self._timer_running}")

    def _countdown(self):
        logging.debug("countdown")
        while self.seconds > 0 and self._timer_running:
            logging.debug("Remaining seconds: {}".format(self.seconds))
            # Aktualisiere die verbleibende Zeit
            self.seconds -= 1
            # Berechne die verbleibenden Minuten und Sekunden
            self.remaining_minutes = self.seconds // 60
            remaining_seconds = self.seconds % 60
            # Rufe die Callback-Funktion auf, um die verbleibende Zeit an die GUI zurückzugeben
            self.callback(self.remaining_minutes, remaining_seconds)
            logging.debug("Remaining Minutes: {}, Remaining Seconds: {}".format(self.remaining_minutes,remaining_seconds))
            # Warte 1 Sekunde, bevor die Methode erneut aufgerufen wird
            time.sleep(1)

        # Timer stoppen, wenn die Zeit abgelaufen ist
        if self.seconds == 0:
            self.stop()
