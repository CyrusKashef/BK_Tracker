'''
Created on Sep 16, 2021

@author: Cyrus
'''

######################
### PYTHON IMPORTS ###
######################

import tkinter as tk
import threading
import time
import os
import mmap
import json
from math import ceil

##############################
### CONFIGURABLE VARIABLES ###
##############################

try:
    with open("GUI_Config.json", "r") as j:
        config_dict = json.load(j)
    UPDATE_PROCESS = config_dict["UPDATE_PROCESS"]
    FONT_SIZE = config_dict["FONT_SIZE"]
    APP_BACKGROUND_COLOR = config_dict["APP_BACKGROUND_COLOR"]
    NOT_FOUND_BACKGROUND_COLOR = config_dict["NOT_FOUND_BACKGROUND_COLOR"]
    FOUND_BACKGROUND_COLOR = config_dict["FOUND_BACKGROUND_COLOR"]
    IMAGES_PER_ROW = config_dict["IMAGES_PER_ROW"]
except Exception as e:
    UPDATE_PROCESS = "Manual"
    FONT_SIZE = 20
    APP_BACKGROUND_COLOR = None
    NOT_FOUND_BACKGROUND_COLOR = "Red"
    FOUND_BACKGROUND_COLOR = "Blue"
    IMAGES_PER_ROW = 5

with open("World_Dict.json", "r") as j:
    world_dict = json.load(j)

with open("Move_Dict.json", "r") as j:
    move_dict = json.load(j)

######################
### MISC VARIABLES ###
######################

VERSION_NUM = "0.1"

###########
### GUI ###
###########

class App():
    def __init__(self, save_file="Banjo-Kazooie.eep", bg_color=APP_BACKGROUND_COLOR):
        self.app_window = tk.Tk()
        self.app_window.winfo_toplevel().title(f"Banjo-Kazooie Tracker v{VERSION_NUM}")
        self.app_window.config(bg=bg_color)
        self.cwd = f"{os.getcwd()}/"
        self.save_file_path = f"{self.cwd}{save_file}"
        self.move_image_dir = f"{self.cwd}Images/Moves/"
        self.world_image_dir = f"{self.cwd}Images/Worlds/"
        self.jiggies_image_dir = f"{self.cwd}Images/Jiggies/"
        self.empty_honeycombs_image_dir = f"{self.cwd}Images/Empty_Honeycombs/"
        self.collectables_image_dir = f"{self.cwd}Images/Collectables/"
        self.app_image_list = []
        self.jiggy_dict = {}
        self.empty_honeycomb_dict = {}
        self.mumbo_token_dict = {}
        self.best_note_dict = {}
        self.world_collectables_dict = {}
        self.current_save_file = 1
        self.current_world_name = "00_Spiral_Mountain"
        self._default_world_collectables()
        self.max_row_count = ceil(12 / IMAGES_PER_ROW)

    class App_Image():
        def __init__(self, window, img_path, bg_color=APP_BACKGROUND_COLOR):
            self.img = tk.PhotoImage(file=img_path)
            self.label = tk.Label(window, image=self.img)
            self.label.config(bg=bg_color)

        def _grid(self, row=0, col=0):
            self.label.grid(row=row, column=col)
        
        def _pack(self):
            self.label.pack()
        
        def _pack_alone(self, ipadx=10, ipady=10, expand=True, fill='both'):
            self.label.pack(ipadx=ipadx, ipady=ipady, expand=expand, fill=fill)
        
        def _pack_with_other(self, ipadx=10, ipady=10, expand=True, fill='both', side='left'):
            self.label.pack(ipadx=ipadx, ipady=ipady, expand=expand, fill=fill, side=side)

    class App_Flip_Image():
        def __init__(self, window, img1_path, img2_path, save_file_index, active_value, bg_color=APP_BACKGROUND_COLOR):
            self.img1 = tk.PhotoImage(file=img1_path)
            self.img2 = tk.PhotoImage(file=img2_path)
            self.active_value = active_value
            self.save_file_index = save_file_index
            self.label = tk.Label(window, image=self.img1)
            self.label.config(bg=bg_color)

        def _grid(self, row=0, col=0):
            self.label.grid(row=row, column=col)

        def _check_for_update(self, save_file_content):
            index_val = save_file_content[self.save_file_index]
            if(index_val == self.active_value):
                self.label.configure(image=self.img2)
            else:
                self.label.configure(image=self.img1)

    class App_Variable_Text():
        def __init__(self, window, variable, font_color, font_size=FONT_SIZE, bg_color=APP_BACKGROUND_COLOR):
            self.text = tk.StringVar()
            self.text.set(str(variable))
            self.label = tk.Label(window, textvariable=self.text, foreground=font_color, font=("Arial",font_size))
            self.label.config(bg=bg_color)

        def _grid(self, row=0, col=0):
            self.label.grid(row=row, column=col)

        def _update_text(self):
            self.text.set(str(self.variable))
    
    class App_Image_Button():
        def __init__(self, window, button_text, image1, image2, image_start=1, master=None):
            self.window = window
            self.text = button_text
            self.image1 = tk.PhotoImage(file=image1)
            self.image2 = tk.PhotoImage(file=image2)
            self.current = image_start
            self.button = tk.Button(window, text=button_text, image=self.image1, bg=APP_BACKGROUND_COLOR, command=self.flip_image)
            self.master = master

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
                self.master.current_world_name = self.text
                self.master._world_collectables()
                self.master._select_world()
            elif(self.master.current_world_name != self.text):
                self.button.configure(image=self.image1)
                self.current = 1

        def grid_button(self, row, column):
            self.row = row
            self.column = column
            self.button.grid(row=self.row, column=self.column)
    
    class App_Counter_Image_Button():
        def __init__(self, window, button_text, image_dir, curr_image_num=0, max_image_num=30, master=None):
            self.window = window
            self.text = button_text
            self.images = []
            image_count = 0
            for image_file in os.listdir(image_dir):
                image = tk.PhotoImage(file=f"{image_dir}{image_file}")
                self.images.append(image)
                image_count += 1
                if(image_count > max_image_num):
                    break
            self.curr_image_num = curr_image_num
            self.button = tk.Button(window, text=button_text, image=self.images[curr_image_num], bg=APP_BACKGROUND_COLOR, command=self.next_image)
            self.master = master
            if(curr_image_num > 0):
                self.button.configure(bg=NOT_FOUND_BACKGROUND_COLOR)
            else:
                self.button.configure(bg=FOUND_BACKGROUND_COLOR)

        def next_image(self):
            if(self.curr_image_num > 0):
                self.curr_image_num -= 1
                self.button.configure(image=self.images[self.curr_image_num])
                self.master.world_collectables_dict[f"{self.master.current_world_name}_{self.text}"] -= 1
                if(self.curr_image_num == 0):
                    self.button.configure(bg=FOUND_BACKGROUND_COLOR)

        def grid_button(self, row, column):
            self.row = row
            self.column = column
            self.button.grid(row=self.row, column=self.column)
    
    class App_Auto_Image_Button():
        def __init__(self, window, button_text, image1, image2, save_file_index, active_value, image_start=1, master=None):
            self.window = window
            self.text = button_text
            self.image1 = tk.PhotoImage(file=image1)
            self.image2 = tk.PhotoImage(file=image2)
            self.current = image_start
            self.active_value = active_value
            self.save_file_index = save_file_index
            if(self.current == 1):
                self.button = tk.Button(window, text=button_text, image=self.image1, command=self.flip_image, bg=NOT_FOUND_BACKGROUND_COLOR)
            else:
                self.button = tk.Button(window, text=button_text, image=self.image2, command=self.flip_image, bg=FOUND_BACKGROUND_COLOR)
            self.master = master

        def set_image(self, image_num):
            if(image_num == 1):
                self.button.configure(image=self.image1)
                self.button.configure(bg=NOT_FOUND_BACKGROUND_COLOR)
                self.current = 1
            else:
                self.button.configure(image=self.image2)
                self.button.configure(bg=FOUND_BACKGROUND_COLOR)
                self.current = 2

        def flip_image(self):
            if(self.current == 1):
                self.button.configure(image=self.image2)
                self.button.configure(bg=FOUND_BACKGROUND_COLOR)
                self.current = 2
                self.master.world_collectables_dict[self.text] = 2
            elif(self.master.current_world_name != self.text):
                self.button.configure(image=self.image1)
                self.button.configure(bg=NOT_FOUND_BACKGROUND_COLOR)
                self.current = 1
                self.master.world_collectables_dict[self.text] = 1

        def grid_button(self, row, column):
            self.row = row
            self.column = column
            self.button.grid(row=self.row, column=self.column)

        def _check_for_update(self, save_file_content):
            index_val = save_file_content[self.save_file_index]
            if(index_val == self.active_value):
                self.label.configure(image=self.img2)
            else:
                self.label.configure(image=self.img1)

    def _read_save_file(self):
        with open(self.save_file_path, "rb") as sf:
            file_bytes = sf.read()
        return file_bytes

    def _obtain_save_file_data(self, save_file=1):
        file_bytes = self._read_save_file()
        save_file_index = None
        for index in range(0, (len(file_bytes.hex())//2)-32, 0x78):
            if(save_file == file_bytes[index+1]):
                save_file_index = index
                break
        if(save_file_index):
            pass
        else:
            # error
            pass
    
    def _save_file_window(self):
        self.save_file_frame = tk.Frame(self.app_window, bg=APP_BACKGROUND_COLOR)
        self.save_file_frame.grid(row=0, column=0)
        save_file_label = tk.Label(self.save_file_frame, text="Which Save File Are You Using?", font=("Arial Bold", FONT_SIZE), padx=15, bg=APP_BACKGROUND_COLOR)
        save_file_label.grid(row=0, column=0)
        save_file_var = tk.IntVar()
        save_file_var.set(self.current_save_file)
        save_file_entry = tk.Entry(self.save_file_frame, textvariable=save_file_var, font=("Arial Bold", FONT_SIZE), width=2)
        save_file_entry.grid(row=0, column=1)
    
    def _moves_window(self):
        self.moves_frame = tk.Frame(self.app_window, bg=APP_BACKGROUND_COLOR)
        self.moves_frame.grid(row=1, column=0)
        move_count = 0
        for move in move_dict:
#             move_image = self.App_Flip_Image(self.moves_frame,
#                                         img1_path=f"{self.move_image_dir}{move}_Dark.png",
#                                         img2_path=f"{self.move_image_dir}{move}_Light.png",
#                                         save_file_index=move_dict[move]["Save_File_Index"],
#                                         active_value=move_dict[move]["Active_Value"])
            move_image = self.App_Auto_Image_Button(self.moves_frame,
                                                     button_text=move,
                                                     image1=f"{self.move_image_dir}{move}_Dark.png",
                                                     image2=f"{self.move_image_dir}{move}_Light.png",
                                                     save_file_index=move_dict[move]["Save_File_Index"],
                                                     active_value=move_dict[move]["Active_Value"],
                                                     image_start=1,
                                                     master=self)
            #move_image._grid(row=(move_count // IMAGES_PER_ROW), col=(move_count % IMAGES_PER_ROW))
            move_image.grid_button(row=(move_count // IMAGES_PER_ROW), column=(move_count % IMAGES_PER_ROW))
            move_count += 1
            self.app_image_list.append(move_image)
    
    def _totals(self):
#         self.totals_frame = tk.Frame(self.app_window, bg=APP_BACKGROUND_COLOR)
#         #self.totals_frame.pack()
#         self.totals_frame.grid(row=2, column=0)
#         collectable_counter = 0
#         collectable_list = []
#         for collectable in collectable_dict:
#             collectable_label = tk.Label(self.totals_frame, text=collectable, font=("Arial Bold", FONT_SIZE), padx=15, foreground=collectable_dict[collectable]["Font_Color"], bg=APP_BACKGROUND_COLOR)
#             collectable_label.grid(row=0, column=collectable_counter)
#             collectable_count = self.App_Variable_Text(self.totals_frame,
#                                                        collectable_dict[collectable]["Variable"],
#                                                        collectable_dict[collectable]["Font_Color"])
#             collectable_count._grid(row=1, col=collectable_counter)
#             collectable_list.append(collectable_count)
#             collectable_counter += 1
        pass
    
    def _default_world_collectables(self):
        for world in world_dict:
            for jiggy in world_dict[world]["Jiggies"]:
                if(jiggy.startswith("No_")):
                    self.world_collectables_dict[jiggy] = 2
                else:
                    self.world_collectables_dict[jiggy] = 1
            for empty_honeycomb in world_dict[world]["Empty_Honeycombs"]:
                if(empty_honeycomb.startswith("No_")):
                    self.world_collectables_dict[empty_honeycomb] = 2
                else:
                    self.world_collectables_dict[empty_honeycomb] = 1
            self.world_collectables_dict[f"{world}_Mumbo_Token"] = world_dict[world]["Mumbo_Token_Count"]
    
    def _world_collectables(self):
        self.world_frames = tk.Frame(self.app_window, bg=APP_BACKGROUND_COLOR)
        self.world_frames.grid(row=3, column=0)
        world_count = 0
        self.world_image_list = []
        #world_frame = tk.LabelFrame(self.world_frames, text=f"{(self.current_world_name.split('_', 1)[1]).replace('_',' ')}", bg=APP_BACKGROUND_COLOR)
        world_frame = tk.LabelFrame(self.world_frames, bg=APP_BACKGROUND_COLOR)
        world_frame.grid(row=(world_count//2), column=(world_count%2))
        item_count = 0
        for jiggy in world_dict[self.current_world_name]["Jiggies"]:
            try:
                jiggy_image = self.App_Auto_Image_Button(world_frame,
                                                         button_text=jiggy,
                                                         image1=f"{self.jiggies_image_dir}{jiggy}_Dark.png",
                                                         image2=f"{self.jiggies_image_dir}{jiggy}_Light.png",
                                                         save_file_index=0,
                                                         active_value=world_dict[self.current_world_name]["Jiggies"][jiggy],
                                                         image_start=self.world_collectables_dict[jiggy],
                                                         master=self)
            except tk.TclError:
                jiggy_image = self.App_Auto_Image_Button(world_frame,
                                                         button_text=jiggy,
                                                         image1=f"{self.jiggies_image_dir}Jiggy_Dark.png",
                                                         image2=f"{self.jiggies_image_dir}Jiggy_Light.png",
                                                         save_file_index=0,
                                                         active_value=world_dict[self.current_world_name]["Jiggies"][jiggy],
                                                         image_start=self.world_collectables_dict[jiggy],
                                                         master=self)
            jiggy_image.grid_button(row=(item_count // IMAGES_PER_ROW), column=(item_count % IMAGES_PER_ROW))
            item_count += 1
            self.world_image_list.append(jiggy_image)
        for empty_honeycomb in world_dict[self.current_world_name]["Empty_Honeycombs"]:
            try:
                empty_honeycomb_image = self.App_Auto_Image_Button(world_frame,
                                                         button_text=empty_honeycomb,
                                                         image1=f"{self.empty_honeycombs_image_dir}{empty_honeycomb}_Dark.png",
                                                         image2=f"{self.empty_honeycombs_image_dir}{empty_honeycomb}_Light.png",
                                                         save_file_index=0,
                                                         active_value=world_dict[self.current_world_name]["Empty_Honeycombs"][empty_honeycomb],
                                                         image_start=self.world_collectables_dict[empty_honeycomb],
                                                         master=self)
            except tk.TclError:
                empty_honeycomb_image = self.App_Auto_Image_Button(world_frame,
                                                         button_text=empty_honeycomb,
                                                         image1=f"{self.empty_honeycombs_image_dir}Empty_Honeycomb_Dark.png",
                                                         image2=f"{self.empty_honeycombs_image_dir}Empty_Honeycomb_Light.png",
                                                         save_file_index=0,
                                                         active_value=world_dict[self.current_world_name]["Empty_Honeycombs"][empty_honeycomb],
                                                         image_start=self.world_collectables_dict[empty_honeycomb],
                                                         master=self)
            empty_honeycomb_image.grid_button(row=(item_count // IMAGES_PER_ROW), column=(item_count % IMAGES_PER_ROW))
            item_count += 1
            self.world_image_list.append(empty_honeycomb_image)
        if(len(world_dict[self.current_world_name]["Mumbo_Tokens"]) > 0):
            mumbo_token_image = self.App_Counter_Image_Button(world_frame,
                                                              "Mumbo_Token",
                                                              f"{self.cwd}Images/Mumbo_Tokens/",
                                                              curr_image_num=self.world_collectables_dict[f"{self.current_world_name}_Mumbo_Token"],
                                                              max_image_num=len(world_dict[self.current_world_name]["Mumbo_Tokens"]),
                                                              master=self)
            mumbo_token_image.grid_button(row=(item_count // IMAGES_PER_ROW), column=(item_count % IMAGES_PER_ROW))
            item_count += 1
            self.world_image_list.append(mumbo_token_image)
        if(ceil(item_count / IMAGES_PER_ROW) < self.max_row_count):
            for empty_row_count in range(self.max_row_count - ceil(item_count / IMAGES_PER_ROW)):
                empty_space_image = self.App_Image(world_frame,
                                                   f"{self.collectables_image_dir}Empty.png",
                                                   bg_color=APP_BACKGROUND_COLOR)
                empty_space_image._grid(row=((item_count // IMAGES_PER_ROW) + empty_row_count + 1), col=0)
                self.world_image_list.append(empty_space_image)
        world_count += 1
    
    def _select_world(self):
        self.world_buttons = tk.Frame(self.app_window, bg=APP_BACKGROUND_COLOR)
        self.world_buttons.grid(row=4, column=0)
        world_counter = 0
        world_button_list = []
        for world in world_dict:
            world_button = self.App_Image_Button(window=self.world_buttons,
                                                 button_text=world,
                                                 image1=f"{self.world_image_dir}{world}.png",
                                                 image2=f"{self.world_image_dir}{world}_Dark.png",
                                                 master=self)
            if(world_counter == 10):
                world_button.grid_button(row=(world_counter // IMAGES_PER_ROW), column=(IMAGES_PER_ROW // 2))
            else:
                world_button.grid_button(row=(world_counter // IMAGES_PER_ROW), column=(world_counter % IMAGES_PER_ROW))
            if(self.current_world_name == world):
                world_button.set_image(image_num=2)
            else:
                world_button.set_image(image_num=1)
            world_button_list.append(world_button)
            world_counter += 1
    
    def _show_window(self):
        if(UPDATE_PROCESS == "PJ64"):
            self._save_file_window()
        
        #############
        ### MOVES ###
        #############
        self._moves_window()

        ###################
        ### TOTAL COUNT ###
        ###################
        # JIGGY COUNT | EMPTY HONEYCOMB COUNT | MUMBO TOKEN COUNT | BEST NOTE SCORE
        self._totals()

        ##########################
        ### WORLD COLLECTABLES ###
        ##########################
        # ORIG WORLD -> NEW WORLD
        # 10 JIGGIES
        # 2 EMPTY HONEYCOMBS | MUMBO TOKEN COUNT/TOTAL | BEST NOTE SCORE
        self._world_collectables()

        ####################
        ### SELECT WORLD ###
        ####################
        
        self._select_world()

        #######################
        ### WORLD ENTRANCES ###
        #######################

        # Threading
        if(UPDATE_PROCESS == "PJ64"):
            update_thread = threading.Thread(target=self._read_save_file)
            update_thread.start()
        # Close Window
        self.app_window.protocol("WM_DELETE_WINDOW", self.app_window.destroy)
        # Main Loop
        self.app_window.mainloop()

app = App()
app._show_window()