import tkinter as tk
from tkinter import ttk, messagebox
from settings import settings
import os
import json

class ItemCreator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Item Creator")
        self.root.geometry("700x300")

        self.optionsframe = tk.Frame(self.root)
        self.optionsframe.columnconfigure(0, weight=1)

        # variables
        self.id_var = tk.StringVar()
        self.id_var.trace_add("write", self.update_name_form_id)
        self.name_var = tk.StringVar()
        self.type_var = tk.StringVar(value="Equipment")
        self.type_var.trace_add("write", self.toggle_equipment_fields)

        self.item_id_label = tk.Label(self.optionsframe, text="Item ID")
        self.item_id_label.grid(row=0, column=0, sticky="we")

        self.item_id_entry = tk.Entry(self.optionsframe, textvariable=self.id_var)
        self.item_id_entry.grid(row=0, column=1, sticky=tk.W+tk.E)

        self.item_name_label = tk.Label(self.optionsframe, text="Item Name")
        self.item_name_label.grid(row=1, column=0, sticky=tk.W+tk.E)

        self.item_name_entry = tk.Entry(self.optionsframe, textvariable=self.name_var)
        self.item_name_entry.grid(row=1, column=1, sticky=tk.W+tk.E)

        self.description_label = tk.Label(self.optionsframe, text="Description")
        self.description_label.grid(row=2, column=0, sticky="we")

        self.description_entry = tk.Entry(self.optionsframe)
        self.description_entry.grid(row=2, column=1, sticky="we")

        self.slot_selection_label = tk.Label(self.optionsframe, text="Equipment Slot")
        self.slot_selection_label.grid(row=3, column=0, sticky="we")

        self.slot_selection_dropdown = ttk.Combobox(self.optionsframe, values=["helmet", "chestplate", "pants", "boots", "weapon", "amulet", "ring"], state="readonly")
        self.slot_selection_dropdown.grid(row=3, column=1, sticky="we")

        self.type_selection_dropdown_label = tk.Label(self.optionsframe, text="Type")
        self.type_selection_dropdown_label.grid(row=4, column=0)

        self.type_selection_dropdown = ttk.Combobox(self.optionsframe, values=["Equipment", "Item", "Consumable"], state="readonly", textvariable=self.type_var)
        self.type_selection_dropdown.grid(row=4, column=1, sticky="we")

        self.sprite_coordinates_label = tk.Label(self.optionsframe, text="Sprite Sheet Coordinates (x, y)px")
        self.sprite_coordinates_label.grid(row=5, column=0)

        self.sprite_coordinates_frame = tk.Frame(self.optionsframe)
        self.sprite_coordinates_frame.grid(row=5, column=1)
        self.x = tk.IntVar(value=0)
        self.y = tk.IntVar(value=0)
        self.sprite_coordinates_x = tk.Entry(self.sprite_coordinates_frame, textvariable=self.x)
        self.sprite_coordinates_x.grid(row=0, column=0)
        self.sprite_coordinates_x = tk.Entry(self.sprite_coordinates_frame, textvariable=self.y)
        self.sprite_coordinates_x.grid(row=0, column=1)


        self.add_stat_btn = tk.Button(self.optionsframe, text="Add Stat", command=self.add_stat)
        self.add_stat_btn.grid(row=6, column=0, sticky="we", columnspan=2)

        self.stats_frame = tk.Frame(self.optionsframe)
        self.stats_frame.grid(row=7, column=0, sticky="we", columnspan=2)
        self.rows = []

        self.save_btn = tk.Button(self.optionsframe, text="Save in JSON", command=self.save_to_json, bg="lightgreen")
        self.save_btn.grid(row=8, column=0, sticky="we", columnspan=2)

        self.optionsframe.pack(fill="x", padx=10, pady=10)
        self.toggle_equipment_fields()
        self.root.mainloop()

    def update_name_form_id(self, *args):
        '''makes form the item ids like max_hp names like Max Hp'''
        id = self.id_var.get()
        name = id.replace("_", " ").title()
        self.name_var.set(name)
    
    def toggle_equipment_fields(self, *args):
        current_type = self.type_var.get().lower()
        if current_type == "equipment":
            self.slot_selection_dropdown.config(state="readonly")
            self.add_stat_btn.config(state="normal")
        else:
            self.slot_selection_dropdown.set("")
            self.slot_selection_dropdown.config(state="disabled")
            self.add_stat_btn.config(state="disabled")

    def add_stat(self):
        row = StatRow(self.stats_frame)
        self.rows.append(row)
    
    def save_to_json(self):
        item_id = self.id_var.get().strip()
        if not item_id:
            messagebox.showerror("Error", "no item id found")
            return

        item_type = self.type_var.get().lower()

        new_item = { # base item structure in JSON
            "name": self.name_var.get().strip(),
            "type": item_type,
            "sprite": {
                "x": self.x.get(),
                "y": self.y.get()
            },
            "description": self.description_entry.get().strip()
        }

        if item_type == "equipment": # only equipment has stats & slots var
            slot = self.slot_selection_dropdown.get()
            if slot:
                new_item["slot"] = slot
            
            stats = {}
            for row in self.rows:
                if row.frame.winfo_exists():
                    stat = row.stat_options.get()
                    if stat:
                        try: # if someone entered , instead of .
                            value = row.value.get()
                            stats[stat] = int(value) if value.is_integer() else value
                        except tk.TclError:
                            messagebox.showerror("Error", "coundnt parse the stat, entered , instead of .")
                            return
            
            if stats:
                new_item["stats"] = stats
            
        json_file_path = settings.ASSET_DIR / "data" / "items.json"
        try:
            if os.path.exists(json_file_path):
                with open(json_file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            else:
                data = {}
        except json.JSONDecodeError:
            messagebox.showerror("Error", "the items.json couldnt be read, it may contain errors")
            return

        data[item_id] = new_item
        try:
            with open(json_file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            messagebox.showinfo("Sucess", str(new_item))
        except Exception as e:
            messagebox.showerror("Error", f"Couldn't save data {e}")


class StatRow:
    def __init__(self, parent):
        self.frame = tk.Frame(parent)
        self.frame.pack(fill="x", expand=True)

        self.stat_options = ttk.Combobox(self.frame, values=["max_hp", "defence", "attack_range", "cooldown"])
        self.stat_options.pack(side="left")

        self.value = tk.DoubleVar(value=0.0)
        self.stat_value = tk.Entry(self.frame, textvariable=self.value)
        self.stat_value.pack(side="left")

        self.delete_stat_btn = tk.Button(self.frame, text="Delete Stat", command=self.delete)
        self.delete_stat_btn.pack(side="left")
    
    def delete(self):
        self.frame.destroy()

ItemCreator()