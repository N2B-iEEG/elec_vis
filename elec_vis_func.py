import os
import tkinter as tk
import tkinter.filedialog
from PIL import Image, ImageFont, ImageDraw

def elec_vis_file_select():
    global patient_name, path_tbl, path_t1
    path_tbl = ''
    path_t1  = ''

    win = tk.Tk()
    win.title('N2B elec_vis file dialog')
    win.resizable(True, True)
    win.geometry('800x400')

    tk.Label(win, text='Patient name').grid(row=0, column=0, sticky='w')
    df_name = tk.StringVar()
    df_name.set("TWH")
    patient_name_entry = tk.Entry(win, textvariable=df_name)
    patient_name_entry.grid(row=0, column=1, sticky='w')

    tbl_label = tk.Label(win, text='')
    t1_label  = tk.Label(win, text='')
    tbl_label.grid(row=1, column=1, sticky='w')
    t1_label.grid(row=2, column=1, sticky='w')

    def elec_tbl_cmd():
        global path_tbl
        path_tbl = tk.filedialog.askopenfilename()
        tbl_label.config(text = path_tbl)
    tk.Button(win, text = 'Select electrode table\n(must contain channel name and coordinates in native & MNI space)', 
    command=elec_tbl_cmd).grid(row=1, column=0, sticky='w')

    def t1_cmd():
        global path_t1
        path_t1 = tk.filedialog.askopenfilename()
        t1_label.config(text = path_t1)
    tk.Button(win, text = "Select the patient's T1-weighted MR\n(brain.mgz if using FreeSurfer for preprocessing)", 
    command=t1_cmd).grid(row=2, column=0, sticky='w')

    # Button for closing
    def close_cmd():
        global patient_name
        patient_name = patient_name_entry.get()
        if path_tbl == "":
            tk.messagebox.showerror('Error', 'Error: no electrode table is selected!')
        if path_t1 == "":
            tk.messagebox.showerror('Error', 'Error: no T1 scan is selected!')
        if path_tbl != "" and path_t1 != "":
            win.destroy()
    tk.Button(win, text="OK", command=close_cmd).grid(row=5, column=1, sticky='w')

    tk.mainloop()

    return patient_name, path_tbl, path_t1

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
        space_name = img_name.split('_')[2]
        space_name = os.path.splitext(space_name)[0]

        img          = Image.open(img_path)
        img_box      = img.getbbox()
        img          = img.crop(img_box)

        new_img = Image.new("RGBA", img.size, "WHITE") # Create a white rgba background
        new_img.paste(img, (0, 0), img)              # Paste the image on the background. Go to the links given below for details.
        img = new_img
        
        img_width    = img.size[0]
        img_height   = img.size[1]
        font_size = min(img_width, img_height) / 20

        img_draw     = ImageDraw.Draw(img)
        font         = ImageFont.truetype('arial.ttf', int(font_size))
        text         = '\n\n'.join(['Patient name:\n    '+ patient_name, 
        'Electrode name:\n    ' + elec_name, 
        'Brain space:\n    ' + space_name])

        img_draw.multiline_text((img_width/2, img_height/2), 
        text, 
        font = font, fill = (0, 0, 0))
        img.save(img_path)