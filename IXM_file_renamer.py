''' This interface sends Unix commands to run folder restructuring.'''

from __future__ import print_function
import argparse
import os
import utils
from datetime import datetime


# A Function to convert from IXM timepoint based subfolder to well subfolder
def timepoint_to_well(input_path):

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

            if str(name).find('.tif') > 0:
                # str(name).find('*'+'.tif') > 0
                print("tif file found!")
                all_src_images = utils.make_filelist_wells(path, 's')
                
            # else:
            #     continue

    print ("the all source images are: ", all_src_images)
    # date = str(input_path.split('/')[-3])
    # date_format = ''.join(date.split('-'))
    # print("date format is: ", date_format)
    # PID_date = 'PID' + date_format + '_'
    # print("The experiment id is: ", PID_date)
    # list_all_files = os.listdir(input_path)
    # print("List of all files are: ", list_all_files)

    # TODO: add PID_date to beginning of the file names
    # for file in list_all_files:
    #
    #     new_file_name = PID_date + file
    #     print("new file name is: ", new_file_name)
    #     source = os.path.join(input_path, file)
    #     destination = os.path.join(input_path, new_file_name)
    #     # os.rename(source, destination)

    ixm_name = 'LBCP191204-DNDA10_A05_s1_w277FB402F-217D-4F57-A0FF-D8C516901226.tif'
    robo3_name_check = 'PIDdate_ExptName_Timepoint_Hours-BurstIndex_Well_MontageNumber_Channel_TimeIncrement_DepthIndex_DepthIncrement.tif'
    list_ixm_tokens = ixm_name.split('_')
    map3x3 = {'s1':'1', 's2':'2', 's3':'3', 's4':'6', 's5':'5', 's6':'4', 's7':'7', 's8':'8', 's9':'9'}
    robo3_generated = '_'.join(['PIDdate', list_ixm_tokens[0], list_ixm_tokens[-1].split('.')[0], '0-0',
                                list_ixm_tokens[1], map3x3[list_ixm_tokens[2]], list_ixm_tokens[3][0:2], '0', '0',
                                '0.tif'])
    print("Robo3 file format: ", robo3_generated)

    # plate_id = utils.get_plate_id(list_all_files)
    # print("Plate IDs are: ", plate_id)
    # for well in valid_wells:
    #     print("we are on well: ", well)
    #     for timepoint in valid_timepoints:
    #         image_stack_list = utils.make_filelist(input_path, well)
    #
    #     print("the image_stack_list is: ", image_stack_list)

    return

def main():
    """
    Args:

    """

    if new_structure == 'to_robo0':
        timepoint_to_well(INPUT_PATH)

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
