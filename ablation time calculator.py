import math
from tkinter import *

# for creating .exe file: pyinstaller --onefile -w ablation time calculator.py

# Dictionaries for containing coefficients

shape_list = ['round', 'square', 'rectangle']
material_dict = {'enter': '0','glass': '0.02', 'metal': '0.01125', 'plastic': '0.01856', 'diamond': '0.00057'} #mm^3/s
hw_dict = {'stage': '1', 'scanner': '0.25'}
wl_dict = {'IR 1030 nm': '1', 'GREEN 515 nm': '3', 'UV 355 nm': '10'}
op_dict = {'F-Theta': '1', 'obj 20x': '2', 'obj 50x': '5'}
through_dict = {'yes': '1', 'no': '2'}
units_of_time_dict = {'sec': '1', 'min': '60', 'hr': '3600'}
units_of_depth_dict = {'mm': '1', '\u03BCm': '0.001', 'nm': '0.000001'}
units_of_dia_dict = {'mm': '1', '\u03BCm': '0.001', 'nm': '0.000001'}

# Function for clearing the contents of all entry boxes

def clear_all() :
    number_field.delete(0, END)
    rate_field.delete(0, END)
    diameter_field.delete(0, END)
    depth_field.delete(0, END)
    time_field.delete(0, END)
    number_field.focus_set()

def clear_number() :
    time_field.delete(0, END)
    number_field.delete(0, END)
    number_field.focus_set()

def calculate_abliation_time():
    time_field.delete(0, END)
    number = int(number_field.get())
    rate = float(rate_field.get())
    diameter = str(diameter_field.get())
    depth = float(depth_field.get())
    shape_field = str(clicked_shape.get())
    material_field = str(clicked_material.get())
    hw_field =  str(clicked_hw.get())
    wl_field =  str(clicked_wl.get())
    op_field =  str(clicked_op.get())
    through_field = str(clicked_through.get())
    units_of_time_field = str(clicked_units_of_time.get())
    units_of_depth_field = str(clicked_units_of_depth.get())
    units_of_dia_field = str(clicked_units_of_dia.get())

    # Calculates volume

    depth_coef = units_of_depth_dict[units_of_depth_field]
    depth_coef = float(depth_coef)

    dia_coef = units_of_dia_dict[units_of_dia_field]
    dia_coef = float(dia_coef)

    if shape_field == shape_list[0]:
        diameter = float(diameter)*dia_coef
        vol = math.pi*((float(diameter)/2)**2)*depth*depth_coef*number
    elif shape_field == shape_list[1]:
        diameter = float(diameter)*dia_coef
        vol = (float(diameter)**2)*number*depth*depth_coef
    elif shape_field == shape_list[2]:
        diameter = diameter.split(', ')
        vol = float(diameter[0])*float(diameter[1])*(dia_coef**2)*number*depth*depth_coef

# Calculates speed

    if material_field == 'enter':
        material_coef = rate
    else:
        material_coef = material_dict[material_field]
        material_coef = float(material_coef)

    hw_coef = hw_dict[hw_field]
    hw_coef = float(hw_coef)

    wl_coef = wl_dict[wl_field]
    wl_coef = float(wl_coef)

    op_coef = op_dict[op_field]
    op_coef = float(op_coef)

    through_coef = through_dict[through_field]
    through_coef = float(through_coef)

    units_of_time_coef = units_of_time_dict[units_of_time_field]
    units_of_time_coef = float(units_of_time_coef)

    speed = (material_coef * units_of_time_coef)/(hw_coef * wl_coef * op_coef * through_coef )

    # Calculates estimated time

    time_cal = round(vol / speed, 3) 

    # insert method inserting the value in the text entry box.
    time_field.insert('end', time_cal)


# Driver code
if __name__ == '__main__' :
   
    # Create a GUI window
    root = Tk()
   
    # Set the background colour of GUI window
    root.configure(background = 'snow3')
   
    # Set the configuration of GUI window
    root.geometry('680x540')
   
    # set the name of tkinter GUI window
    root.title('Abliation Time Calculator') 
       
    # Create a Principal Amount : label
    label1 = Label(root, text = 'Number of holes : ', fg = 'black', bg = 'yellow')
    label2 = Label(root, text = ' Through : ', fg = 'black', bg = 'yellow')
    label3 = Label(root, text = ' Shape : ', fg = 'black', bg = 'yellow')
    label4 = Label(root, text = 'Diameter(rnd)/Side(sqr)/Side1, Side2(rect) : ', fg = 'black', bg = 'yellow')  
    label5 = Label(root, text = 'Depth : ', fg = 'black', bg = 'yellow')
    label6 = Label(root, text = ' Material : ', fg = 'black', bg = 'yellow')
    label7 = Label(root, text = ' Setup : ', fg = 'black', bg = 'yellow')
    label9 = Label(root, text = ' Estimated time : ', fg = 'black', bg = 'yellow')
    label10 = Label(root, text = ' Rate mm\u00B3/s: ', fg = 'black', bg = 'yellow')

    # grid method is used for placing the widgets at respective positions in table like structure .

    label1.grid(row = 1, column = 0, padx = 10, pady = 10) 
    label2.grid(row = 2, column = 0, padx = 10, pady = 10) 
    label3.grid(row = 3, column = 0, padx = 10, pady = 10)
    label4.grid(row = 4, column = 0, padx = 10, pady = 10)
    label5.grid(row = 5, column = 0, padx = 10, pady = 10)
    label6.grid(row = 6, column = 0, padx = 10, pady = 10)
    label7.grid(row = 7, column = 0, padx = 10, pady = 10)
    label9.grid(row = 9, column = 0, padx = 10, pady = 10)
    label10.grid(row = 6, column = 2, padx = 10, pady = 10)

    clicked_shape = StringVar()
    clicked_shape.set(shape_list[0])

    clicked_material = StringVar()
    clicked_material.set(list(material_dict.keys())[0])

    clicked_hw = StringVar()
    clicked_hw.set(list(hw_dict.keys())[0])

    clicked_wl = StringVar()
    clicked_wl.set(list(wl_dict.keys())[0])

    clicked_op = StringVar()
    clicked_op.set(list(op_dict.keys())[0])

    clicked_through = StringVar()
    clicked_through.set(list(through_dict.keys())[0])

    clicked_units_of_time = StringVar()
    clicked_units_of_time.set(list(units_of_time_dict.keys())[0])

    clicked_units_of_depth = StringVar()
    clicked_units_of_depth.set(list(units_of_depth_dict.keys())[0])

    clicked_units_of_dia = StringVar()
    clicked_units_of_dia.set(list(units_of_dia_dict.keys())[0])

    rate_field = StringVar()
    rate_field.set(list(material_dict.values())[0])

    # Create a entry box for filling or typing the information.

    number_field = Entry(root)
    rate_field = Entry(root, textvariable=rate_field)
    diameter_field = Entry(root) 
    depth_field = Entry(root)
    shape_field = OptionMenu(root, clicked_shape, *shape_list)
    material_field = OptionMenu(root, clicked_material, *material_dict.keys())
    hw_field = OptionMenu(root, clicked_hw, *hw_dict.keys())
    wl_field = OptionMenu(root, clicked_wl, *wl_dict.keys())
    op_field = OptionMenu(root, clicked_op, *op_dict.keys())
    through_field = OptionMenu(root, clicked_through, *through_dict.keys())
    units_of_time_field = OptionMenu(root, clicked_units_of_time, *units_of_time_dict.keys())
    units_of_depth_field = OptionMenu(root, clicked_units_of_depth, *units_of_depth_dict.keys())
    units_of_dia_field = OptionMenu(root, clicked_units_of_dia, *units_of_dia_dict.keys())
    time_field = Entry(root)

    shape_field.config(r=RIDGE, borderwidth=2)
    hw_field.config(r=RIDGE, borderwidth=2)
    wl_field.config(r=RIDGE, borderwidth=2)
    op_field.config(r=RIDGE, borderwidth=2)
    material_field.config(r=RIDGE, borderwidth=2)
    through_field.config(r=RIDGE, borderwidth=2)
    units_of_time_field.config()
    units_of_dia_field.config()
    units_of_depth_field.config()
    number_field.config()
    diameter_field.config()
    depth_field.config()
    time_field.config()
    rate_field.config()
 
    # grid method is used for placing the widgets at respective positions in table like structure .

    number_field.grid(row = 1, column = 1, padx = 10, pady = 10)
    through_field.grid(row = 2, column = 1, padx = 10, pady = 10)
    shape_field.grid(row = 3, column = 1, padx = 10, pady = 10)
    diameter_field.grid(row = 4, column = 1, padx = 10, pady = 10) 
    depth_field.grid(row = 5, column = 1, padx = 10, pady = 10)
    material_field.grid(row = 6, column = 1, padx = 10, pady = 10)
    hw_field.grid(row = 7, column = 1, padx = 10, pady = 10)
    wl_field.grid(row = 7, column = 2, padx = 10, pady = 10)
    op_field.grid(row = 7, column = 3, padx = 10, pady = 10)
    units_of_time_field.grid(row = 9, column = 2, padx = 10, pady = 10, sticky = W)
    units_of_depth_field.grid(row = 5, column = 2, padx = 10, pady = 10, sticky = W)
    units_of_dia_field.grid(row = 4, column = 2, padx = 10, pady = 10, sticky = W)
    time_field.grid(row = 9, column = 1, padx = 10, pady = 10)
    rate_field.grid(row = 6, column = 3, padx = 10, pady = 10)
    
    # Buttons attached to functions

    button1 = Button(root, text = 'Submit', bg = 'forest green', activebackground='yellow', 
                     fg = 'black', command = calculate_abliation_time)
   
    button2 = Button(root, text = 'Clear all', bg = 'red', activebackground='forest green',
                     fg = 'black', command = clear_all)

    button3 = Button(root, text = 'Clear number of holes', bg = 'red', activebackground='forest green',
                     fg = 'black', command = clear_number)
   
    button1.grid(row = 8, column = 1, pady = 10)
    button2.grid(row = 10, column = 1, pady = 10)
    button3.grid(row = 1, column = 2, pady = 10)
 
    # Start the GUI 
    root.mainloop()
