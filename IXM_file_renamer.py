''' This interface sends Unix commands to run folder restructuring.'''

from __future__ import print_function
import argparse
import os
import utils
import shutil
from datetime import datetime


def montage_mapper(list_ixm_tokens, NxN):

    tile_number = 0
    map3x3 = {'s1':'1', 's2':'2', 's3':'3', 's4':'6', 's5':'5', 's6':'4', 's7':'7', 's8':'8', 's9':'9'}
    map4x4 = {'s1':'1', 's2':'2', 's3':'3', 's4':'4', 's5':'8', 's6':'7', 's7':'6', 's8':'5', 's9':'9',
              's10':'10', 's11':'11', 's12':'12', 's13':'16', 's14':'15', 's15':'14', 's16':'13'}
    if NxN == 4:
        tile_number = map4x4[list_ixm_tokens[2]]
    elif NxN == 3:
        tile_number = map3x3[list_ixm_tokens[2]]
    return tile_number


def path_generator(input_path, output_path):
    all_src_images = []
    output_path_expt_well = []

    print("The input path is: ", input_path)
    for dir in os.walk(input_path, topdown=True):
        # import pprint
        # pprint.pprint(dir)
        # print("We are walking in: ", dir)

        for name in dir[1:]:
            # print("the name is: ", name)
            # path = os.path.join(input_path, dir[])
            # print("The path is: ", path)
            if str(name).find('TimePoint') > 0:
                # print("the name is: ", name)
                print("We are in: ", dir[0])
                print (" The sub directory name is: ", name[0])

                source_path = os.path.join(input_path, dir[0], name[0])
                print("The path is: ", source_path)
            if str(name).find(".DS_Store") > 0:
                thumb_path = os.path.join(input_path, dir[0], name[4])
                print("thumbnail file found at:", thumb_path)
                # list(name).pop(4)
                # # thumb_path_abs = os.path.abspath(thumb_path)
                # print("Thumb file removed.", name)

            if str(name).find('.tif') > 0:
                # str(name).find('*'+'.tif') > 0
                print("tif file found!")
                all_src_images = utils.make_filelist_wells(source_path, 's')

    original_file_name = os.path.basename(all_src_images[0])
    list_ixm_tokens = original_file_name.split('_')
    output_path_expt = os.path.join(output_path, list_ixm_tokens[0])
    utils.create_dir(output_path_expt)
    output_path_expt_well = os.path.join(output_path_expt, list_ixm_tokens[1])
    utils.create_dir(output_path_expt_well)

    return all_src_images, output_path_expt_well


# A Function to convert from IXM timepoint based subfolder to well subfolder
def timepoint_to_well(input_path, output_path):
    """    Robo0: PIDdate_ExptName_Timepoint_Hours
    -BurstIndex_Well_MontageNumber_Channel_TimeIncrement_DepthIndex_DepthIncrement.tif
    """
    date = []
    date_format = []
    all_src_images, output_path_expt_well = path_generator(input_path, output_path)

    print ("the all source images are: ", all_src_images)
    base_path = os.path.basename(all_src_images[0])
    print("base path is: ", base_path)
    date = str(all_src_images[0].split('/')[-3])
    date_format = ''.join(date.split('-'))
    # print("date format is: ", date_format)
    PID_date = 'PID' + date_format
    # print("The experiment id is: ", PID_date)
    # TODO: time point
    time_point = 'T' + str(all_src_images[0].split('/')[-2]).split('_')[1]
    print("The time point is: ", time_point)

    # list_all_files_base = os.path.basename(all_src_images[:])
    # print("List of all files are: ", list_all_files_base)

    all_dest_images = []
    NxN = []
    tiles = [all_src_images[i].split('/')[-1].split('_')[2].split('s')[1] for i in range(0, len(all_src_images))]
    tiles_int = [int(x) for x in tiles]
    # print("The tiles are: ", tiles_int)
    max_tile = max(tiles_int)
    # print("max tile is: ", max_tile)
    if max_tile == 16:
        NxN = 4
    elif max_tile == 9:
        NxN = 3

    for file in all_src_images:
        original_file_name = os.path.basename(file)
        list_ixm_tokens = original_file_name.split('_')
        channel = list_ixm_tokens[-1].split('.')[0].split('-')[0]
        # print("list_ixm_tokens for the files are: ", list_ixm_tokens)
        tile_number = montage_mapper(list_ixm_tokens, NxN)
        new_file_name = os.path.join(output_path_expt_well, '_'.join([PID_date, list_ixm_tokens[0], time_point,
                                                                      '0-0', list_ixm_tokens[1],
                                                                      tile_number, channel, '0',
                                                                      '0', '0.tif']))
        all_dest_images.append(new_file_name)
        shutil.copy(file, new_file_name)

    print("The new name is: ", all_dest_images)

    return


def main():
    """
    Args:

    """

    timepoint_to_well(INPUT_PATH, OUTPUT_PATH)

    return


if __name__ == '__main__':
    # Receiving the variables from the XML script, parse them, initialize them, and verify the paths exist.

    # ----Parser-----------------------
    parser = argparse.ArgumentParser(description="Folder Restructuring.")
    parser.add_argument("input_path", help="The path to parent folder.")
    parser.add_argument("output_path", help="Output path for the new folder structure.")

    args = parser.parse_args()

    # ----Initialize parameters------------------
    INPUT_PATH = args.input_path
    print("The input path is: ", INPUT_PATH)
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
