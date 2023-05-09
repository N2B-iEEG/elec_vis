import os
import numpy as np
from PIL import Image, ImageFont, ImageDraw
from tkinter import Tk, Label, Entry, Button, StringVar, font
from tkinter.filedialog import askopenfilename
from typing import Tuple

def elec_vis_file_select() -> Tuple[str, str, str]:

    def select_table_file():
        file_path = askopenfilename(filetypes=[('Table files', '*.csv *.xlsx')])
        path_tbl.set(file_path)
        if file_path:  # Check if a file was selected
            btn_table['text'] = file_path

    def select_t1_file():
        file_path = askopenfilename(filetypes=[('Nifti files', '*.nii *.nii.gz *.mgh *.mgz')])
        path_t1.set(file_path)
        if file_path:  # Check if a file was selected
            btn_t1['text'] = file_path

    def submit():
        root.destroy()

    root = Tk()
    root.title('N2B elec_vis file dialog')
    root.resizable(True, True)
    root.geometry('1000x300')

    # Define the font
    customFont = font.Font(family="Georgia", size=30)

    patient_name = StringVar(value='TWH')
    path_tbl = StringVar()
    path_t1 = StringVar()

    Label(root, text="Patient name", font=customFont).grid(row=0, column=0)
    Entry(root, textvariable=patient_name, font=customFont).grid(row=0, column=1)

    Label(root, text="Select elec table", font=customFont).grid(row=1, column=0)
    btn_table = Button(root, text="Browse...", command=select_table_file, font=customFont)
    btn_table.grid(row=1, column=1)

    Label(root, text="Select patient T1", font=customFont).grid(row=2, column=0)
    btn_t1 = Button(root, text="Browse...", command=select_t1_file, font=customFont)
    btn_t1.grid(row=2, column=1)

    Button(root, text="Submit", command=submit, font=customFont).grid(row=3, columnspan=2)

    root.mainloop()

    return patient_name.get(), path_tbl.get(), path_t1.get()

def elec_vis_annotate(output_dir):
    img_path_list = []
    for root, dirs, files in os.walk(output_dir):
        for name in files:
            if name.split('.')[1] == 'png':
                img_path_list.append(os.path.join(root, name))

    for img_path in img_path_list:
        img_name     = os.path.split(img_path)[1]
        patient_name = img_name.split('_')[0]
        elec_name    = img_name.split('_')[1]
        space_name   = img_name.split('_')[2]
        space_name   = os.path.splitext(space_name)[0]

        img          = Image.open(img_path)
        img_box      = img.getbbox()
        img          = img.crop(img_box)
        
        if np.array(img).shape[2] == 4: # If image output is .png with transparent background
            new_img = Image.new("RGBA", img.size, "BLACK") # Create a black rgba background
            new_img.paste(img, (0, 0), img)                # Paste the image on the background.
            img = new_img
        
        img_width    = img.size[0]
        img_height   = img.size[1]
        font_size = min(img_width, img_height) / 25

        img_draw     = ImageDraw.Draw(img)
        font         = ImageFont.truetype('SourceCodePro-Regular.ttf', int(font_size))
        text         = '\n\n'.join(['Patient name:\n    '+ patient_name, 
        'Electrode name:\n    ' + elec_name, 
        'Brain space:\n    ' + space_name])

        img_draw.multiline_text((img_width/2, img_height/2), 
        text,
        font = font, 
        fill = (255, 255, 255) # Font color = white (against black background)
        )
        img.save(img_path)