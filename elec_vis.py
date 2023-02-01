import os
import shutil
import pandas as pd
import subprocess
import json
import tkinter as tk

from elec_vis_func import *

elec_vis_dir  = os.path.dirname(os.path.realpath(__file__))
MRIcroGL_path = os.path.join(elec_vis_dir, 'MRIcroGL', 'MRIcroGL')
script_path   = os.path.join(elec_vis_dir, 'MRIcroGL_script.py')

# Specify patient name and select electrode table & T1 scan
patient_name, path_tbl, path_t1 = elec_vis_file_select()

# Create elec_vis folder at electrode table location
tbl_head = os.path.split(path_tbl)[0]
output_dir = os.path.join(tbl_head, (patient_name + '_elec_vis'))
if os.path.exists(output_dir): # If exists already
    shutil.rmtree(output_dir)  # delete the folder
os.mkdir(output_dir)

output_dir_native = os.path.join(output_dir, 'native')
os.mkdir(output_dir_native)

output_dir_MNI = os.path.join(output_dir, 'MNI')
os.mkdir(output_dir_MNI)

output_dir_MNI_AAL = os.path.join(output_dir, 'MNI_AAL')
os.mkdir(output_dir_MNI_AAL)

# Read electrode table
tbl_data = pd.read_excel(path_tbl)
tbl_data = tbl_data.reset_index()  # make sure indexes pair with number of rows

# Convert table to a nested list
tbl_list = []
for index, row in tbl_data.iterrows():
    ch_name = row['channel']
    elec_cor_list = [ch_name, 
    row['native_x'], row['native_y'], row['native_z'], 
    row['MNI_x'],    row['MNI_y'],    row['MNI_z']]
    tbl_list.append(elec_cor_list)

# Get screen size
monitor_file = open('monitor.json')
monitor_dict = json.load(monitor_file)

# Create temporary json for subprocess to access
data_dict = {
    "elec_vis_dir"       : elec_vis_dir,
    "patient_name"       : patient_name,
    "path_tbl"           : path_tbl,
    "path_t1"            : path_t1,
    "output_dir_native"  : output_dir_native,
    "output_dir_MNI"     : output_dir_MNI,
    "output_dir_MNI_AAL" : output_dir_MNI_AAL,
    "tbl_list"           : tbl_list
}
data_dict.update(monitor_dict)
json_object = json.dumps(data_dict, indent = 4)
with open("tmp.json", "w") as tmp:
    tmp.write(json_object)

# Call subprocess
subprocess.call([MRIcroGL_path, script_path])

# Move tmp.json to output directory
shutil.move('tmp.json', os.path.join(output_dir, 'parameters.json'))

elec_vis_annotate(output_dir)