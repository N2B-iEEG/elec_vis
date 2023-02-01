# Initialization
import gl
import os
import json

tmp_file = open('tmp.json')
data = json.load(tmp_file)

keys = [
    "elec_vis_dir", "patient_name",
    "path_tbl", "path_t1",
    "output_dir_native", "output_dir_MNI", "output_dir_MNI_AAL",
    "tbl_list",
    "monitor_width", "monitor_height"]

(elec_vis_dir, patient_name, 
path_tbl, path_t1, 
output_dir_native, output_dir_MNI, output_dir_MNI_AAL,
tbl_list,
monitor_width, monitor_height) = [
    data.get(key) for key in keys]

# Width : height = 3:4, determine size
if monitor_height < monitor_width * 0.75:
    window_height = monitor_height
    window_width = round(window_height * 0.75)
else:
    window_width = monitor_width
    window_height = round(window_width * 1.33)

MNI_path = os.path.join('.', 'MRIcroGL', 'Resources',
                        'standard', 'mni152.nii.gz')
AAL_path = os.path.join('.', 'MRIcroGL', 'Resources', 'atlas', 'aal.nii.gz')

# Set up canvas
gl.resetdefaults()
gl.windowposition(0, 0, window_width, window_height)

gl.backcolor(255, 255, 255) # Background color: white
gl.colorbarposition(0)      # Disable color bar
gl.toolformvisible(0)       # Hide tool panel
gl.scriptformvisible(0)     # Hide script panel
gl.bmpzoom(1)               # Save bitmaps at screen resolution
gl.linecolor(225, 0, 225)   # Crosshair color (purple)
gl.linewidth(5)             # Crosshair width

# Visualization in native space
gl.loadimage(path_t1)
for elec_list in tbl_list:
    elec_name = elec_list[0]
    output_path = os.path.join(
        output_dir_native, (patient_name + '_' + elec_name + '_native.png'))
    gl.orthoviewmm(elec_list[1], elec_list[2], elec_list[3])
    gl.savebmp(output_path)

# Visualization in MNI space
gl.loadimage(MNI_path)
gl.minmax(0, 20, 80)

for elec_list in tbl_list:
    elec_name = elec_list[0]
    output_path = os.path.join(
        output_dir_MNI, (patient_name + '_' + elec_name + '_MNI.png'))
    gl.orthoviewmm(elec_list[4], elec_list[5], elec_list[6])
    gl.savebmp(output_path)

# Visualization in MNI space with AAL
gl.overlayload(AAL_path)
for elec_list in tbl_list:
    elec_name = elec_list[0]
    output_path = os.path.join(
        output_dir_MNI_AAL, (patient_name + '_' + elec_name + '_MNI-AAL.png'))
    gl.orthoviewmm(elec_list[4], elec_list[5], elec_list[6])
    gl.savebmp(output_path)

gl.quit()
