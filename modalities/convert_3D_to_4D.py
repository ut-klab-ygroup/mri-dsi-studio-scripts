import os
import re
import numpy as np
# import nibabel as nib


def sort_nii_files(files):
    """
    Sorting NIfTI files based on the number in their filename
    Parameters:
        - path to the folder or directory where .nii files are located
    Return:
        - shows sorted list with all .nii images
    
    """
    files.sort(key=lambda file: int(re.search(r'_(\d+)\.nii$', file).group(1)) 
               if re.search(r'_(\d+)\.nii$', file) else 0)
    return files


def process_subject_folder(folder_path):
    """Process all NIfTI files in a given folder and save a combined 4D NIfTI file."""

    nii_files = [f for f in os.listdir(folder_path) if f.endswith('.nii')]
    if not nii_files:
        print(f'No NIfTi files found in {folder_path}')
        return  # skiping if no NIfTI files found

    show_files = sort_nii_files(nii_files) # sort files because normaly they are not sorted
    print(show_files)
    
    example_img = nib.load(os.path.join(folder_path, nii_files[0])) # loading the first image to get the shape and affine because needs to be used in next steps
    data_shape = example_img.get_fdata().shape
    print(data_shape)

    if len(data_shape) == 4:
        print(f'Skipping {folder_path} as it already contains a 4D NIfTI file.')
        return # skipping

    combined_data = np.zeros(data_shape + (len(nii_files),))   # Initialize the 4D numpy array
    
    for i, file in enumerate(nii_files): # Load each file and add its data to the combined_data array
        img = nib.load(os.path.join(folder_path, file))
        combined_data[..., i] = img.get_fdata()

    new_img = nib.Nifti1Image(combined_data, affine=example_img.affine)

    subject_name = os.path.basename(folder_path).split('_')[0]

    output_filename = os.path.join(folder_path, f'{subject_name}_4D.nii')
    nib.save(new_img, output_filename)

# base_directory = '../test_DSI'

# for subject_folder in os.listdir(base_directory):
#     folder_path = os.path.join(base_directory, subject_folder)
#     if os.path.isdir(folder_path):
#         process_subject_folder(folder_path)