'''
Created on Aug 19, 2021

@author: Cyrus
'''
import tkinter as tk
import tkinter.filedialog
import os

BK_Tracker_Version = "0.1"

class App():
    def __init__(self):
        self.app_window = tk.Tk()
        self.app_window.winfo_toplevel().title(f"Banjo-Kazooie Tracker v{BK_Tracker_Version}")

    class App_Button():
        def __init__(self, window, button_text, cmd):
            self.button = tk.Button(window, text=button_text, command=cmd)

        def pack_button(self):
            self.button.pack()

        def grid_button(self, row, column):
            self.row = row
            self.column = column
            self.button.grid(row=self.row, column=self.column)

    class App_Image_Button():
        def __init__(self, window, button_text, image1, image2, image_start=1):
            self.window = window
            self.text = button_text
            self.image1 = tk.PhotoImage(file=image1)
            self.image2 = tk.PhotoImage(file=image2)
            self.current = image_start
            self.button = tk.Button(window, text=button_text, image=self.image1, command=self.flip_image)

        def set_image(self, image_num):
            if(image_num == 1):
                self.button.configure(image=self.image1)
                self.current = 1
            else:
                self.button.configure(image=self.image2)
                self.current = 2

        def flip_image(self):
            if(self.current == 1):
                self.button.configure(image=self.image2)
                self.current = 2
            else:
                self.button.configure(image=self.image1)
                self.current = 1

        def grid_button(self, row, column):
            self.row = row
            self.column = column
            self.button.grid(row=self.row, column=self.column)

    class App_Selectable_Image_Button():
        def __init__(self, window, button_text, height=6, width=21):
            self.window = window
            self.text = button_text
            self.height = height
            self.width = width
            self.button = tk.Button(window, text=button_text, height=height, width=width, command=self.select_image)
        
        def select_image(self):
            cwd = os.getcwd() + "\\BK_Images\\Worlds\\"
            image_file = tk.filedialog.askopenfilename(initialdir=cwd, title="Select World Image", filetype =(("Images","*.png"),("all files","*.*")) )
            if(not image_file):
                self.reset_button()
            else:
                self.image = tk.PhotoImage(file=image_file)
                self.button.configure(image=self.image)
                self.button.configure(height=95)
                self.button.configure(width=150)

        def grid_button(self, row, column):
            self.row = row
            self.column = column
            self.button.grid(row=self.row, column=self.column)
        
        def reset_button(self):
            self.button.configure(image="")
            self.button.configure(text=self.text)
            self.button.configure(height=self.height)
            self.button.configure(width=self.width)

    def all_set_image1(self):
        for button in [self.talon_trot, self.beak_buster, self.shock_jump,
                       self.egg_firing, self.flight, self.beak_bomb,
                       self.wonderwing, self.turbo_talon_trot, self.wading_boots]:
            button.set_image(1)

    def all_set_image2(self):
        for button in [self.talon_trot, self.beak_buster, self.shock_jump,
                       self.egg_firing, self.flight, self.beak_bomb,
                       self.wonderwing, self.turbo_talon_trot, self.wading_boots]:
            button.set_image(2)

    def reset_world_images(self):
        for button in [self.first_world, self.second_world, self.third_world,
                       self.fourth_world, self.fifth_world, self.sixth_world,
                       self.seventh_world, self.eighth_world, self.ninth_world]:
            button.reset_button()

    def image_buttons_moves(self, moves_image_dir):
        ### LEARNED MOVES ###
        self.learned_moves_frame = tk.LabelFrame(self.app_window, text="Learned Moves", width=400, height=400, padx=5, pady=5)
        self.learned_moves_frame.grid(row=0, column=0, sticky="nsew")
        self.talon_trot = self.App_Image_Button(window=self.learned_moves_frame,
                                    button_text="Talon Trot",
                                    image1=f"{moves_image_dir}Talon_Trot_Light.png",
                                    image2=f"{moves_image_dir}Talon_Trot_Dark.png")
        self.talon_trot.grid_button(row=0, column=0)
        self.beak_buster = self.App_Image_Button(window=self.learned_moves_frame,
                                    button_text="Beak Buster",
                                    image1=f"{moves_image_dir}Beak_Buster_Light.png",
                                    image2=f"{moves_image_dir}Beak_Buster_Dark.png")
        self.beak_buster.grid_button(row=0, column=1)
        self.shock_jump = self.App_Image_Button(window=self.learned_moves_frame,
                                    button_text="Spring Shock Jump",
                                    image1=f"{moves_image_dir}Shock_Spring_Jump_Light.png",
                                    image2=f"{moves_image_dir}Shock_Spring_Jump_Dark.png")
        self.shock_jump.grid_button(row=0, column=2)
        self.egg_firing = self.App_Image_Button(window=self.learned_moves_frame,
                                    button_text="Egg Firing",
                                    image1=f"{moves_image_dir}Egg_Firing_Light.png",
                                    image2=f"{moves_image_dir}Egg_Firing_Dark.png")
        self.egg_firing.grid_button(row=1, column=0)
        self.flight = self.App_Image_Button(window=self.learned_moves_frame,
                                    button_text="Flight",
                                    image1=f"{moves_image_dir}Flight_Light.png",
                                    image2=f"{moves_image_dir}Flight_Dark.png")
        self.flight.grid_button(row=1, column=1)
        self.beak_bomb = self.App_Image_Button(window=self.learned_moves_frame,
                                    button_text="Beak Bomb",
                                    image1=f"{moves_image_dir}Beak_Bomb_Light.png",
                                    image2=f"{moves_image_dir}Beak_Bomb_Dark.png")
        self.beak_bomb.grid_button(row=1, column=2)
        self.wonderwing = self.App_Image_Button(window=self.learned_moves_frame,
                                    button_text="Wonderwing",
                                    image1=f"{moves_image_dir}Wonderwing_Light.png",
                                    image2=f"{moves_image_dir}Wonderwing_Dark.png")
        self.wonderwing.grid_button(row=2, column=0)
        self.turbo_talon_trot = self.App_Image_Button(window=self.learned_moves_frame,
                                    button_text="Turbo Talon Trot",
                                    image1=f"{moves_image_dir}Turbo_Trainers_Light.png",
                                    image2=f"{moves_image_dir}Turbo_Trainers_Dark.png")
        self.turbo_talon_trot.grid_button(row=2, column=1)
        self.wading_boots = self.App_Image_Button(window=self.learned_moves_frame,
                                    button_text="Wading Boots",
                                    image1=f"{moves_image_dir}Wading_Boots_Light.png",
                                    image2=f"{moves_image_dir}Wading_Boots_Dark.png")
        self.wading_boots.grid_button(row=2, column=2)
        self.all_highlight = self.App_Button(window=self.learned_moves_frame,
                                       button_text="Highlight All",
                                       cmd=self.all_set_image1)
        self.all_highlight.grid_button(row=3, column=0)
        self.all_darkened = self.App_Button(window=self.learned_moves_frame,
                                       button_text="Darken All",
                                       cmd=self.all_set_image2)
        self.all_darkened.grid_button(row=3, column=2)
        ### WORLD ORDER ###
        self.world_order_frame = tk.LabelFrame(self.app_window, text="World Order", width=400, height=400, padx=5, pady=5)
        self.world_order_frame.grid(row=0, column=1, sticky="nsew")
        self.first_world = self.App_Selectable_Image_Button(self.world_order_frame, "First World")
        self.first_world.grid_button(row=0, column=0)
        self.second_world = self.App_Selectable_Image_Button(self.world_order_frame, "Second World")
        self.second_world.grid_button(row=0, column=1)
        self.third_world = self.App_Selectable_Image_Button(self.world_order_frame, "Third World")
        self.third_world.grid_button(row=0, column=2)
        self.fourth_world = self.App_Selectable_Image_Button(self.world_order_frame, "Fourth World")
        self.fourth_world.grid_button(row=1, column=0)
        self.fifth_world = self.App_Selectable_Image_Button(self.world_order_frame, "Fifth World")
        self.fifth_world.grid_button(row=1, column=1)
        self.sixth_world = self.App_Selectable_Image_Button(self.world_order_frame, "Sixth World")
        self.sixth_world.grid_button(row=1, column=2)
        self.seventh_world = self.App_Selectable_Image_Button(self.world_order_frame, "Seventh World")
        self.seventh_world.grid_button(row=2, column=0)
        self.eighth_world = self.App_Selectable_Image_Button(self.world_order_frame, "Eighth World")
        self.eighth_world.grid_button(row=2, column=1)
        self.ninth_world = self.App_Selectable_Image_Button(self.world_order_frame, "Ninth World")
        self.ninth_world.grid_button(row=2, column=2)
        self.reset_worlds = self.App_Button(window=self.world_order_frame,
                                       button_text="Reset Worlds",
                                       cmd=self.reset_world_images)
        self.reset_worlds.grid_button(row=3, column=1)
        ### Close Window ##
        self.app_window.protocol("WM_DELETE_WINDOW", self.app_window.destroy)
        ### Main Loop ###
        self.app_window.mainloop()

if __name__ == '__main__':
    app = App()
    moves_image_dir = cwd = os.getcwd() + "\\BK_Images\\Moves\\"
    app.image_buttons_moves(moves_image_dir)
