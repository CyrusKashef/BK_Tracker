'''
Created on Aug 19, 2021

@author: Cyrus
'''
import tkinter as tk
import tkinter.filedialog
import os

BK_Tracker_Version = "0.1"

def read_config():
    config_dir = os.getcwd() + "\\bk_tracker_config.ini"
    with open(config_dir, "r") as config_file:
        config_lines = config_file.readlines()
    move_config_option = "1"
    world_config_option = "1"
    for line in config_lines:
        if(line.startswith("Moves_Option=")):
            move_config_option = (line.split("=")[1]).replace(" ", "").replace("\n", "")
        elif(line.startswith("World_Order_Option=")):
            world_config_option = (line.split("=")[1]).replace(" ", "").replace("\n", "")
    return (move_config_option, world_config_option)

class App():
    def __init__(self, bg_color=None):
        self.app_window = tk.Tk()
        self.app_window.winfo_toplevel().title(f"Banjo-Kazooie Tracker v{BK_Tracker_Version}")
        self.app_window.bg_color = bg_color

    class App_Button():
        def __init__(self, window, button_text, cmd):
            self.button = tk.Button(window, text=button_text, command=cmd)
            self.button.config(bg=(window.bg_color))

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
            self.button.config(bg=(window.bg_color))

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

    class App_CheckButton():
        def __init__(self, window, checkbutton_text, default=0, padx=5, pady=5):
            self.value = tk.IntVar(value=default)
            self.checkbutton = tk.Checkbutton(window, text=checkbutton_text, variable=self.value, padx=5, pady=5)

        def grid_checkbutton(self, row, column):
            self.row = row
            self.column = column
            self.checkbutton.grid(row=self.row, column=self.column)
        
        def set_checkbutton(self, value):
            self.value.set(value)
    
    class App_Label():
        def __init__(self, window, label_text, padx=7, pady=7):
            self.text = tk.StringVar()
            self.text.set(label_text)
            self.label = tk.Label(window, text=label_text, padx=padx, pady=pady)

        def grid_label(self, row, column):
            self.row = row
            self.column = column
            self.label.grid(row=self.row, column=self.column)
    
    class App_Image_Label():
        def __init__(self, window, image_path):
            self.image = tk.PhotoImage(file=image_path)
            self.label = tk.Label(window, image=self.image)
            self.label.config(bg=(window.bg_color))

        def grid_label(self, row, column):
            self.row = row
            self.column = column
            self.label.grid(row=self.row, column=self.column)
    
    class App_Options_Menu():
        def __init__(self, window, options_dict, default=None):
            self.str_var = tk.StringVar(window)
            self.option_menu = tk.OptionMenu(window, self.str_var, *options_dict)
            if(default):
                self.str_var.set(default)
        
        def set_option(self, option):
            self.str_var.set(option)

        def grid_option_menu(self, row, column):
            self.row = row
            self.column = column
            self.option_menu.grid(row=self.row, column=self.column)

    ### MOVE CHECKBOXES ###

    def clear_checkboxes(self):
        for checkbox in [self.talon_trot, self.beak_buster, self.shock_jump,
                         self.egg_firing, self.flight, self.beak_bomb,
                         self.wonderwing, self.turbo_talon_trot, self.wading_boots]:
            checkbox.set_checkbutton(0)

    def move_checkboxes(self):
        self.learned_moves_frame = tk.LabelFrame(self.app_window, text="Learned Moves", width=400, height=400, padx=5, pady=5)
        self.learned_moves_frame.grid(row=0, column=0, sticky="nsew")
        self.learned_moves_frame.bg_color = self.app_window.bg_color
        self.talon_trot = self.App_CheckButton(self.learned_moves_frame, "Talon Trot")
        self.talon_trot.grid_checkbutton(row=0, column=0)
        self.beak_buster = self.App_CheckButton(self.learned_moves_frame, "Beak Buster")
        self.beak_buster.grid_checkbutton(row=1, column=0)
        self.shock_jump = self.App_CheckButton(self.learned_moves_frame, "Spring Shock Jump")
        self.shock_jump.grid_checkbutton(row=2, column=0)
        self.egg_firing = self.App_CheckButton(self.learned_moves_frame, "Egg Firing")
        self.egg_firing.grid_checkbutton(row=3, column=0)
        self.flight = self.App_CheckButton(self.learned_moves_frame, "Flight")
        self.flight.grid_checkbutton(row=4, column=0)
        self.beak_bomb = self.App_CheckButton(self.learned_moves_frame, "Beak Bomb")
        self.beak_bomb.grid_checkbutton(row=5, column=0)
        self.wonderwing = self.App_CheckButton(self.learned_moves_frame, "Wonderwing")
        self.wonderwing.grid_checkbutton(row=6, column=0)
        self.turbo_talon_trot = self.App_CheckButton(self.learned_moves_frame, "Running Shoes")
        self.turbo_talon_trot.grid_checkbutton(row=7, column=0)
        self.wading_boots = self.App_CheckButton(self.learned_moves_frame, "Wading Boots")
        self.wading_boots.grid_checkbutton(row=8, column=0)
        self.uncheck_all = self.App_Button(window=self.learned_moves_frame,
                                       button_text="Uncheck All",
                                       cmd=self.clear_checkboxes)
        self.uncheck_all.grid_button(row=10, column=0)

    ### WORLD ORDER OPTION MENU ###

    def reset_option_menus(self):
        for option_menu in [self.first_world_options, self.second_world_options, self.third_world_options,
                            self.fourth_world_options, self.fifth_world_options, self.sixth_world_options,
                            self.seventh_world_options, self.eighth_world_options, self.ninth_world_options]:
            option_menu.set_option("Unknown")

    def world_order_option_menu(self):
        self.world_order_frame = tk.LabelFrame(self.app_window, text="World Order", width=400, height=400, padx=5, pady=5)
        self.world_order_frame.grid(row=0, column=1, sticky="nsew")
        options_dict = ["Unknown", "MM - Mumbo's Mountain", "TTC - Treasure Trove Cove", "CC - Clanker's Cavern",
                        "BGS - Bubblegloop Swamp", "FP - Freezeezy Peak", "GV - Gobi's Valley",
                        "MMM - Mad Monster Mansion", "RBB - Rusty Bucket Bay", "CCW - Click Clock Wood"]
        self.first_world_label = self.App_Label(self.world_order_frame, label_text="Mumbo's Mountain ->")
        self.first_world_label.grid_label(row=0, column=0)
        self.first_world_options = self.App_Options_Menu(self.world_order_frame, options_dict, default="Unknown")
        self.first_world_options.grid_option_menu(row=0, column=1)
        self.second_world_label = self.App_Label(self.world_order_frame, label_text="Treasure Trove Cove ->")
        self.second_world_label.grid_label(row=1, column=0)
        self.second_world_options = self.App_Options_Menu(self.world_order_frame, options_dict, default="Unknown")
        self.second_world_options.grid_option_menu(row=1, column=1)
        self.third_world_label = self.App_Label(self.world_order_frame, label_text="Clanker's Cavern ->")
        self.third_world_label.grid_label(row=2, column=0)
        self.third_world_options = self.App_Options_Menu(self.world_order_frame, options_dict, default="Unknown")
        self.third_world_options.grid_option_menu(row=2, column=1)
        self.fourth_world_label = self.App_Label(self.world_order_frame, label_text="Bubblegloop Swamp ->")
        self.fourth_world_label.grid_label(row=3, column=0)
        self.fourth_world_options = self.App_Options_Menu(self.world_order_frame, options_dict, default="Unknown")
        self.fourth_world_options.grid_option_menu(row=3, column=1)
        self.fifth_world_label = self.App_Label(self.world_order_frame, label_text="Freezeezy Peak ->")
        self.fifth_world_label.grid_label(row=4, column=0)
        self.fifth_world_options = self.App_Options_Menu(self.world_order_frame, options_dict, default="Unknown")
        self.fifth_world_options.grid_option_menu(row=4, column=1)
        self.sixth_world_label = self.App_Label(self.world_order_frame, label_text="Gobi's Valley ->")
        self.sixth_world_label.grid_label(row=5, column=0)
        self.sixth_world_options = self.App_Options_Menu(self.world_order_frame, options_dict, default="Unknown")
        self.sixth_world_options.grid_option_menu(row=5, column=1)
        self.seventh_world_label = self.App_Label(self.world_order_frame, label_text="Mad Monster Mansion ->")
        self.seventh_world_label.grid_label(row=6, column=0)
        self.seventh_world_options = self.App_Options_Menu(self.world_order_frame, options_dict, default="Unknown")
        self.seventh_world_options.grid_option_menu(row=6, column=1)
        self.eighth_world_label = self.App_Label(self.world_order_frame, label_text="Rusty Bucket Bay ->")
        self.eighth_world_label.grid_label(row=7, column=0)
        self.eighth_world_options = self.App_Options_Menu(self.world_order_frame, options_dict, default="Unknown")
        self.eighth_world_options.grid_option_menu(row=7, column=1)
        self.ninth_world_label = self.App_Label(self.world_order_frame, label_text="Click Clock Wood ->")
        self.ninth_world_label.grid_label(row=8, column=0)
        self.ninth_world_options = self.App_Options_Menu(self.world_order_frame, options_dict, default="Unknown")
        self.ninth_world_options.grid_option_menu(row=8, column=1)
        self.reset_world_options = self.App_Button(window=self.world_order_frame,
                                       button_text="Reset All",
                                       cmd=self.reset_option_menus)
        self.reset_world_options.grid_button(row=10, column=0)

    ### MOVE IMAGES ###

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

    def move_image_buttons(self, moves_image_dir):
        self.learned_moves_frame = tk.LabelFrame(self.app_window, text="Learned Moves", width=400, height=400, padx=5, pady=5)
        self.learned_moves_frame.grid(row=0, column=0, sticky="nsew")
        self.learned_moves_frame.config(bg=(self.app_window.bg_color))
        self.learned_moves_frame.bg_color = self.app_window.bg_color
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

    ### WORLD ORDER PICTURES ###

    def reset_world_images(self):
        for button in [self.first_world, self.second_world, self.third_world,
                       self.fourth_world, self.fifth_world, self.sixth_world,
                       self.seventh_world, self.eighth_world, self.ninth_world]:
            button.reset_button()

    def world_order_pictures(self):
        self.world_order_frame = tk.LabelFrame(self.app_window, text="World Order", width=400, height=400, padx=5, pady=5)
        self.world_order_frame.grid(row=0, column=1, sticky="nsew")
        self.world_order_frame.config(bg=(self.app_window.bg_color))
        self.world_order_frame.bg_color = self.app_window.bg_color
        self.first_world = self.App_Selectable_Image_Button(self.world_order_frame, "Mumbo's Mountain\nEntrance")
        self.first_world.grid_button(row=0, column=0)
        self.second_world = self.App_Selectable_Image_Button(self.world_order_frame, "Treasure Trove Cove\nEntrance")
        self.second_world.grid_button(row=0, column=1)
        self.third_world = self.App_Selectable_Image_Button(self.world_order_frame, "Clanker's Cavern\nEntrance")
        self.third_world.grid_button(row=0, column=2)
        self.fourth_world = self.App_Selectable_Image_Button(self.world_order_frame, "Bubblegloop Swamp\nEntrance")
        self.fourth_world.grid_button(row=1, column=0)
        self.fifth_world = self.App_Selectable_Image_Button(self.world_order_frame, "Freezeezy Peak\nEntrance")
        self.fifth_world.grid_button(row=1, column=1)
        self.sixth_world = self.App_Selectable_Image_Button(self.world_order_frame, "Gobi's Valley\nEntrance")
        self.sixth_world.grid_button(row=1, column=2)
        self.seventh_world = self.App_Selectable_Image_Button(self.world_order_frame, "Mad Monster Mansion\nEntrance")
        self.seventh_world.grid_button(row=2, column=0)
        self.eighth_world = self.App_Selectable_Image_Button(self.world_order_frame, "Rusty Bucket Bay\nEntrance")
        self.eighth_world.grid_button(row=2, column=1)
        self.ninth_world = self.App_Selectable_Image_Button(self.world_order_frame, "Click Clock Wood\nEntrance")
        self.ninth_world.grid_button(row=2, column=2)
        self.reset_worlds = self.App_Button(window=self.world_order_frame,
                                       button_text="Reset Worlds",
                                       cmd=self.reset_world_images)
        self.reset_worlds.grid_button(row=3, column=1)

    ### MAIN ###

    def main(self, move_config_option, world_config_option):
        if(move_config_option == "1"):
            self.move_checkboxes()
        elif(move_config_option == "2"):
            moves_image_dir = os.getcwd() + "\\BK_Images\\Moves\\"
            self.move_image_buttons(moves_image_dir)
        if(world_config_option == "1"):
            self.world_order_option_menu()
        elif(world_config_option == "2"):
            self.world_order_pictures()
        ### Close Window ##
        self.app_window.protocol("WM_DELETE_WINDOW", self.app_window.destroy)
        ### Main Loop ###
        self.app_window.mainloop()

if __name__ == '__main__':
    (move_config_option, world_config_option) = read_config()
    app = App()#bg_color='Pink')
    app.main(move_config_option, world_config_option)
