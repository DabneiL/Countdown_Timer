import tkinter as tk
from tkinter import PhotoImage
import pygame
import os




class CountdownTimer:
    def __init__(self, root):

        self.root = root
        self.root.title("Countdown Timer by Kishnu Kumar")
        self.root.geometry("800x600")

        image_path = "C:/Users/Dabnei LeBlanc/Desktop/Code Library/Countdown_Timer/b2.gif"

        self.bg_image = PhotoImage(file=image_path)
        self.bg_label = tk.Label(root, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.time_left = 0
        self.is_running = False
        self.laps = []

        self.label = tk.Label(root, font=("Helvetica", 48), fg="red")
        self.label.pack(pady=20)

        self.entry = tk.Entry(root, font=("Helvetica", 24))
        self.entry.pack(pady=10)

        self.start_button = tk.Button(root, text="Start", command=self.start_timer, bg="green", fg="white")
        self.start_button.pack()

        self.lap_button = tk.Button(root, text="Lap", command=self.record_lap, bg="yellow", fg="black")
        self.lap_button.pack()

        self.reset_button = tk.Button(root, text="Reset", command=self.reset_timer, bg="blue", fg="white")
        self.reset_button.pack()


        self.tick_sound = os.path.join("/home/krishna/PycharmProjects/G-project_Countdowntimer", "ticktick.mp3")
        self.timeout_sound = os.path.join("//home/krishna/PycharmProjects/G-project_Countdowntimer", "timeup.mp3")


        pygame.mixer.init()


        self.laps_listbox = tk.Listbox(root, font=("Helvetica", 18), width=40, height=12, justify="center")
        self.laps_listbox.pack(pady=10)

        developers_frame = tk.Frame(root, bg="#292929")
        developers_frame.pack()

        developers_names = ["\nKishnu Kumar\n","\nContact: krrish9783","\n+9173551395"]
        developers_label = tk.Label(developers_frame, text="Developer\n" + "\n".join(developers_names),
                                    font=("Times New Roman", 15), bg="#292929", fg="white",width=40, height=12)
        developers_label.pack(pady=10)

    def start_timer(self):
        if not self.is_running:
            input_time = self.entry.get()
            self.time_left = self.parse_time(input_time)
            if self.time_left > 0:
                self.is_running = True
                self.update_timer()

    def parse_time(time_str):
        try:
            hours, minutes, seconds = map(int, time_str.split(":"))
        except ValueError:
            # Handle the case when the input is not in the expected format
            print("Invalid time format. Please use 'hours:minutes:seconds' format.")
            # You can return a default value or raise an exception here if necessary.
            return None

        return hours, minutes, seconds


    def update_timer(self):
        if self.time_left > 0 and self.is_running:
            self.label.config(text=self.format_time(self.time_left))
            self.time_left -= 1
            self.root.after(1000, self.update_timer)
            self.play_tick_sound()

        elif self.time_left == 0 and self.is_running:
            self.is_running = False
            self.label.config(text="Time's up!", fg="red")
            self.play_timeup_sound()
            self.blink_label()

    def format_time(self, total_seconds):
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def blink_label(self):
        current_color = self.label.cget("background")
        new_color = "red" if current_color == "white" else "white"
        self.label.config(background=new_color)
        self.label.after(500, self.blink_label)

    def play_tick_sound(self):
        pygame.mixer.music.load(self.tick_sound)
        pygame.mixer.music.play(-1)

    def play_timeup_sound(self):
        pygame.mixer.music.load(self.timeout_sound)
        pygame.mixer.music.play()

    def record_lap(self):
        if self.is_running:
            self.laps.append(self.time_left)
            self.update_laps_listbox()

    def update_laps_listbox(self):
        self.laps_listbox.delete(0, tk.END)
        for lap_time in self.laps:
            self.laps_listbox.insert(tk.END, self.format_time(lap_time))

    def reset_timer(self):
        pygame.mixer.music.stop()
        self.is_running = False
        self.time_left = 0
        self.laps = []
        self.label.config(text="")
        self.label.config(fg="black")
        self.entry.delete(0, tk.END)
        self.laps_listbox.delete(0, tk.END)



pygame.mixer.init()

root = tk.Tk()
timer = CountdownTimer(root)
root.mainloop()
