''' This interface sends Unix commands to run folder restructuring.'''

from __future__ import print_function
import argparse
import os
import utils
import shutil
from datetime import datetime


def montage_mapper(list_ixm_tokens, NxN):
    tile_number = 0
    map3x3 = {'s1': '1', 's2': '2', 's3': '3', 's4': '6', 's5': '5', 's6': '4', 's7': '7', 's8': '8', 's9': '9'}
    map4x4 = {'s1': '1', 's2': '2', 's3': '3', 's4': '4', 's5': '8', 's6': '7', 's7': '6', 's8': '5', 's9': '9',
              's10': '10', 's11': '11', 's12': '12', 's13': '16', 's14': '15', 's15': '14', 's16': '13'}
    if NxN == 4:
        tile_number = map4x4[list_ixm_tokens[2]]
    elif NxN == 3:
        tile_number = map3x3[list_ixm_tokens[2]]
    return tile_number


def path_generator(input_path, output_path):
    print("The input path is: ", input_path)

    for dir in os.walk(input_path, topdown=True):

        for name in dir[1:]:
            # print("the name is: ", name)
            # path = os.path.join(input_path, dir[])
            # print("The path is: ", path)

            if str(name).find(".DS_Store") > 0:
                thumb_path = os.path.join(input_path, dir[0], name[0])
                print("thumbnail file found at:", thumb_path)
                # list(name).pop(4)
                # # thumb_path_abs = os.path.abspath(thumb_path)
                # print("Thumb file removed.", name)

            if str(name).find('.tif') > 0:
                # str(name).find('*'+'.tif') > 0
                print("tif file found!")
                source_path_tif = os.path.join(input_path, dir[0], name[0])
                # source_path2 = source_path2.pop(0)

    source_path2 = [os.path.join(input_path, fn[0]) for fn in os.walk(input_path, topdown=True)
                    if (str(fn[0]).find('TimePoint')) > 0]
    if source_path2:
        source_path2 = source_path2.pop(0)
        print("list compression source path is: ", source_path2)

    # source_path_tif = [os.path.join(input_path, fn) for fn in os.walk(input_path, topdown=True)
    #                    if (str(fn[-1]).find('.tif')) > 0]
    # if source_path_tif:
    #     source_path_tif = source_path_tif.pop(0)
    #     print("tif file found at: ", source_path_tif)

    base_file_name = os.path.basename(source_path_tif)
    print("base of the file name is: ", base_file_name)
    list_ixm_tokens = base_file_name.split('_')

    print("list of ixm tokens are: ", list_ixm_tokens)
    output_path_expt = os.path.join(output_path, list_ixm_tokens[0])
    utils.create_dir(output_path_expt)
    output_path_expt_well = os.path.join(output_path_expt, list_ixm_tokens[1])
    utils.create_dir(output_path_expt_well)

    return output_path_expt_well, source_path2


def time_point_generator(all_src_images):
    base_path = os.path.basename(all_src_images[0])
    print("base path is: ", base_path)
    date = str(all_src_images[0].split('/')[-4])
    date_format = ''.join(date.split('-'))
    print("date format is: ", date_format)
    pid_date = 'PID' + date_format
    # print("The experiment id is: ", PID_date)
    # TODO: time point
    time_point = 'T' + str(all_src_images[0].split('/')[-2]).split('_')[1]
    print("The time point is: ", time_point)
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

    return time_point, pid_date, NxN


def rename_ixm(all_src_images, output_path_expt_well, pid_date, time_point, NxN):
    all_dest_images = []

    for file in all_src_images:
        original_file_name = os.path.basename(file)
        list_ixm_tokens = original_file_name.split('_')
        channel = list_ixm_tokens[-1].split('.')[0].split('-')[0]
        # print("list_ixm_tokens for the files are: ", list_ixm_tokens)
        tile_number = montage_mapper(list_ixm_tokens, NxN)
        new_file_name = os.path.join(output_path_expt_well, '_'.join([pid_date, list_ixm_tokens[0], time_point,
                                                                      '0-0', list_ixm_tokens[1],
                                                                      tile_number, channel, '0',
                                                                      '0', '0.tif']))
        all_dest_images.append(new_file_name)

    return all_dest_images


def copier(all_src_images, all_dest_images):
    for file in range(0, len(all_src_images)):
        shutil.copy(all_src_images[file], all_dest_images[file])

    return


# A Function to convert from IXM timepoint based subfolder to well subfolder
def timepoint_to_well(input_path, output_path):
    """    Robo0: PIDdate_ExptName_Timepoint_Hours
    -BurstIndex_Well_MontageNumber_Channel_TimeIncrement_DepthIndex_DepthIncrement.tif
    """

    output_path_expt_well, source_path2 = path_generator(input_path, output_path)
    all_src_images = utils.make_filelist_wells(source_path2, 's')
    print("the all source images are: ", all_src_images)

    time_point, pid_date, NxN = time_point_generator(all_src_images)

    # list_all_files_base = os.path.basename(all_src_images[:])
    # print("List of all files are: ", list_all_files_base)
    all_dest_images = rename_ixm(all_src_images, output_path_expt_well, pid_date, time_point, NxN)

    print("The new names are: ", all_dest_images)

    copier(all_src_images, all_dest_images)
    print("Copying completed!------------------------------------------------------------------")
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
