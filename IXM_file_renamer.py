''' This interface sends Unix commands to run folder restructuring.'''

from __future__ import print_function
import argparse
import os
import utils
import shutil
from datetime import datetime


# A Function to convert from IXM timepoint based subfolder to well subfolder
def timepoint_to_well(input_path, output_path):
    """    Robo0: PIDdate_ExptName_Timepoint_Hours
    -BurstIndex_Well_MontageNumber_Channel_TimeIncrement_DepthIndex_DepthIncrement.tif
    """
    date = []
    date_format = []
    all_src_images = []

    print("The input path is: ", input_path)
    for dir in os.walk(input_path, topdown=True):
        # print("We are walking in: ", dir)

        for name in dir[1:]:
            # print("the name is: ", name)
            # path = os.path.join(input_path, dir[])
            # print("The path is: ", path)
            if str(name).find('TimePoint') > 0:
                print("the name is: ", name)
                print("We are in: ", dir[0])
                print (" The sub directory name is: ", name[0])

                path = os.path.join(input_path, dir[0], name[0])
                print("The path is: ", path)
            if str(name).find(".DS_Store") > 0:
                # list(name).index(".DS_Store")
                thumb_path = os.path.join(input_path, dir[0], name[4])
                print("thumbnail file found at:", thumb_path)
                # list(name).pop(4)
                # # thumb_path_abs = os.path.abspath(thumb_path)
                # print("Thumb file removed.", name)

            if str(name).find('.tif') > 0:
                # str(name).find('*'+'.tif') > 0
                print("tif file found!")
                all_src_images = utils.make_filelist_wells(path, 's')

            # else:
            #     continue

    print ("the all source images are: ", all_src_images)
    base_path = os.path.basename(all_src_images[0])
    print("base path is: ", base_path)
    date = str(path.split('/')[-3])
    date_format = ''.join(date.split('-'))
    print("date format is: ", date_format)
    PID_date = 'PID' + date_format
    print("The experiment id is: ", PID_date)
    # TODO: time point
    time_point = 'T' + str(path.split('/')[-1]).split('_')[1]
    print("The time point is: ", time_point)

    # list_all_files_base = os.path.basename(all_src_images[:])
    # print("List of all files are: ", list_all_files_base)

    all_dest_images = []
    map3x3 = {'s1':'1', 's2':'2', 's3':'3', 's4':'6', 's5':'5', 's6':'4', 's7':'7', 's8':'8', 's9':'9'}
    map4x4 = {'s1':'1', 's2':'2', 's3':'3', 's4':'4', 's5':'8', 's6':'7', 's7':'6', 's8':'5', 's9':'9',
              's10':'10', 's11':'11', 's12':'12', 's13':'16', 's14':'15', 's15':'14', 's16':'13'}

    # TODO: add PID_date to beginning of the file names
    output_path_time = os.path.join(output_path, time_point)
    utils.create_dir(output_path_time)
    for file in all_src_images:

        original_file_name = os.path.basename(file)
        list_ixm_tokens = original_file_name.split('_')
        # print("list_ixm_tokens for the files are: ", list_ixm_tokens)
        new_file_name = os.path.join(output_path_time, '_'.join([PID_date, list_ixm_tokens[0], time_point, '0-0',
                                                     list_ixm_tokens[1], map4x4[list_ixm_tokens[2]],
                                                     list_ixm_tokens[-1].split('.')[0], '0', '0', '0.tif']))
        all_dest_images.append(new_file_name)
        shutil.copy(file, new_file_name)

    # print("The new name is: ", all_dest_images)

    return


def main():
    """
    Args:

    """

    if new_structure == 'to_robo0':
        timepoint_to_well(INPUT_PATH, OUTPUT_PATH)

    return


if __name__ == '__main__':
    # Receiving the variables from the XML script, parse them, initialize them, and verify the paths exist.

    # ----Parser-----------------------
    parser = argparse.ArgumentParser(description="Folder Restructuring.")
    parser.add_argument("input_path", help="The path to parent folder.")
    parser.add_argument("new_structure", help="The new structure you would like to change to.")
    parser.add_argument("output_path", help="Output path for the new folder structure.")

    args = parser.parse_args()

    # ----Initialize parameters------------------
    INPUT_PATH = args.input_path
    print("The input path is: ", INPUT_PATH)
    new_structure = args.new_structure
    print("The new folder structure is: ", new_structure)
    OUTPUT_PATH = args.output_path
    print("The output path is: ", OUTPUT_PATH)

    # ----Confirm given folders exist--
    if not os.path.exists(INPUT_PATH):
        print('Confirm the given path to input folder exists.')
        assert os.path.exists(INPUT_PATH), 'Path to input folder is wrong.'
        if not os.path.exists(OUTPUT_PATH):
            print('Confirm the given path to output exists.')
            assert os.path.abspath(OUTPUT_PATH) != os.path.abspath(
                INPUT_PATH), 'Please provide a unique output path.'

            date_time = datetime.now().strftime("%m-%d-%Y_%H:%M")

    main()
