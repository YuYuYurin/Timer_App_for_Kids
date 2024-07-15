import tkinter as tk
import math
from stopwatch_04 import Stopwatch
import logging

class Timer_GUI:



    def __init__(self, root):

        logging.basicConfig(level=logging.DEBUG)

        self.root = root
        self.root.title("Timer")

        # Leinwand für Timer erstellen
        self.canvas_timer = tk.Canvas(root, width=400, height=400)
        self.canvas_timer.pack()

        # Eingabefeld für Minuten
        self.entry_label = tk.Label(root, text="Minuten:")
        self.entry_label.pack()
        self.entry = tk.Entry(root)
        self.entry.pack()

        # Timer setzen Button
        self.set_timer_button = tk.Button(root, text="Timer setzen", command=self.set_timer)
        self.set_timer_button.pack()
        
        # Timer stop Button
        self.set_timer_button = tk.Button(root, text="stop", command=self.stop_timer) 
        self.set_timer_button.pack()

        # Meldung
        self.result_label = tk.Label(root, text="")
        self.result_label.pack()

        #Initialisierung center_x.. _y, radius
        self.center_x = 200
        self.center_y = 200
        self.radius = 150

        # Initialisiere timer_minutes
        self.timer_minutes = 0
        self.remaining_minutes = 0
        
        # Stopwatch-Instanz
        self.stopwatch = None  
        self._timer_running = False
        '''
        self.stopwatch = Stopwatch(3, self.timer_callback)  
        self.stopwatch.start()
        self._timer_running = True
        '''
        # Aktualisiere den Timer
        self.update_timer() 

    def update_timer(self):
        self.canvas_timer.delete("all")
        # Zeichne den Kreis von Timer
        self.canvas_timer.create_oval(self.center_x - self.radius, self.center_y - self.radius, self.center_x + self.radius, self.center_y + self.radius, outline="black", width=2)

        # Zeichne die Zahlen von 0 bis 60
        for minute in range(0, 61, 5):
            angle = math.radians(-90 + 6 * minute)
            text_x = self.center_x + (self.radius - 20) * math.cos(angle)
            text_y = self.center_y + (self.radius - 20) * math.sin(angle)
            self.canvas_timer.create_text(text_x, text_y, text=str(minute), fill="black", font=("Helvetica", 8), tags="timer_numbers")


        # Zeichne den zweiten Zeiger, der die vom Benutzer eingegebene Zeit zeigt = Startzeiger
        #if self.stopwatch is not None and self._timer_running:
        if self.stopwatch:
            logging.debug(f"Stopwatch vorhanden. Timer läuft: {self.stopwatch._timer_running}")
        if self.stopwatch and self.stopwatch._timer_running:
            logging.debug("update_timer() If_Block")
            remaining_minutes = self.stopwatch.remaining_minutes
            logging.debug(f"update_timer(), Remaining minutes: {remaining_minutes}")
            self.draw_hand(remaining_minutes, "red")
        else:
            self.draw_hand(self.timer_minutes, "red")
            logging.debug("update_timer() Else Block")

        # jede Sekunde update_timer() aufrufen
        self.root.after(1000, self.update_timer)


    def draw_hand(self, remaining_minutes, color):
        logging.debug(f"draw_hand, Remaining_Minutes: {remaining_minutes}")
        angle = math.radians(-90 + 6 * remaining_minutes)

        logging.debug(f"Angle {angle}")
        x = self.center_x + (self.radius - 20) * math.cos(angle)
        y = self.center_y + (self.radius - 20) * math.sin(angle)
        #logging.debug(f"x: {x}, y: {y}")
        self.canvas_timer.create_line(self.center_x, self.center_y, x, y, fill=color, width=2, tags="timer_hand")

    def set_timer(self):
        try:
            logging.debug("set_timer")
            minutes = int(self.entry.get())
            logging.debug(f"Minutes: {minutes}")
            if minutes >= 0 and minutes <= 60:
                self.timer_minutes = minutes
                self.draw_hand(self.timer_minutes, "red")
                logging.debug("draw_hand in set_timer")
                self.stopwatch = Stopwatch(self.timer_minutes, self.timer_callback) # eine Instanz der Stopwatch Klasse
                logging.debug("Stopwatch-Instanz wurde aufgerufen")
                self.result_label.config(text="Timer gesetzt für {} Minuten.".format(minutes))
                self.stopwatch.start()
                logging.debug("start")
                logging.debug(f"self._timer_running: {self._timer_running}")
                self.update_timer()
                logging.debug("update")
            else:
                raise ValueError("Bitte geben Sie eine Zahl zwischen 0 und 60 ein.")
        except ValueError as e:
            self.result_label.config(text=str(e))

    def stop_timer(self):
        if self.stopwatch is not None:
            self.stopwatch.stop()
            logging.debug(f"self._timer_running: {self._timer_running}")
            self.result_label.config(text="Timer gestoppt.")
            self.canvas_timer.delete("timer_hand")  # Lösche den Timerzeiger
        else:
            logging.debug("Stopwatch-Objekt ist nicht initialisiert.")
    
    def timer_callback(self, remaining_minutes, remaining_seconds):
        if remaining_minutes == 0 and remaining_seconds == 0:
            self.result_label.config(text="Timer abgelaufen!")
        else:
            logging.debug(f"timer_callback. Else-Block.Restliche Minuten: {remaining_minutes}, Restliche Sekunden: {remaining_seconds}")
            self.result_label.config(text="noch {} Minuten und {} Sekunden".format(remaining_minutes, remaining_seconds))



# Hauptfenster erstellen
root = tk.Tk()
app = Timer_GUI(root)
root.mainloop()
