__author__ = 'Junghwan Kim'
__copyright__ = 'Copyright 2016-2018 Junghwan Kim. All Rights Reserved.'
__version__ = '1.0.0'

import numpy as np
import os
from PIL import Image, ImageDraw, ImageFont
import shutil
np.set_printoptions(threshold=np.nan)


def main():
    global path, path_result, num

    # Set path
    path = '/home/jkim/NAS/members/jkim/data'

    # Output information
    print '\n----------------------------------------------------------------------------------------------------' \
          '\nCompare Three Images %s' \
          '\n----------------------------------------------------------------------------------------------------' \
          '\nYou set path: %s\n' % (__version__, path)

    # Function
    def append_list(path, list, label):
        for paths, dirs, files in sorted(os.walk(path)):
            for name in sorted(files):
                if name.endswith(label):
                    list.append(name)

        return None

    # New folder
    print '[INFO] Making the result folder...'
    path_result = path + '/results_jkim'
    if not os.path.exists(path_result):
        os.makedirs(path_result)
    else:
        shutil.rmtree(path_result)
        os.makedirs(path_result)
    print '[SUCCESS] Made it successfully.\n'

    # Initialize list
    list1 = []
    list1_fill = []
    list1_line = []
    list2 = []
    list2_fill = []
    list2_line = []
    list3 = []
    list3_fill = []
    list3_line = []

    # Append list
    print '[INFO] Creating the image list. It takes a lot of time. Please wait...'
    append_list(path + '/1/images', list1, '.png')
    append_list(path + '/1/labels', list1_fill, 'fill.png')
    append_list(path + '/1/labels', list1_line, 'line.png')
    append_list(path + '/2/images', list2, '.png')
    append_list(path + '/2/labels', list2_fill, 'fill.png')
    append_list(path + '/2/labels', list2_line, 'line.png')
    append_list(path + '/3/images', list3, '.png')
    append_list(path + '/3/labels', list3_fill, 'fill.png')
    append_list(path + '/3/labels', list3_line, 'line.png')
    print '[SUCCESS] Created all list.\n'

    # Validate list
    print '[INFO] Checking the validation...'
    if len(sorted(list1)) == len(sorted(list2)) == len(sorted(list3))\
            == len(sorted(list1_fill)) == len(sorted(list2_fill)) == len(sorted(list3_fill)) \
            == len(sorted(list1_line)) == len(sorted(list2_line)) == len(sorted(list3_line)):
        pass
    else:
        print '[ERROR] List size is different.'
        exit(1)

    for i in range(0, len(sorted(list1))):
        if sorted(list1[i][:26]) == sorted(list2[i][:26]) == sorted(list3[i][:26]):
            pass
        else:
            print '[ERROR] File name is different: ' + list1[i] + ', ' + list2[i] + ', ' + list3[i]
            exit(1)

    for i in range(0, len(sorted(list1_fill))):
        if sorted(list1_fill[i][:26]) == sorted(list2_fill[i][:26]) == sorted(list3_fill[i][:26]):
            pass
        else:
            print '[ERROR] File name is different: ' + list1_fill[i] + ', ' + list2_fill[i] + ', ' + list3_fill[i]
            exit(1)

    for i in range(0, len(sorted(list1_line))):
        if sorted(list1_line[i][:26]) == sorted(list2_line[i][:26]) == sorted(list3_line[i][:26]):
            pass
        else:
            print '[ERROR] File name is different: ' + list1_line[i] + ', ' + list2_line[i] + ', ' + list3_line[i]
            exit(1)
    print '[SUCCESS] Passed the validation.\n'

    # Overlay anatomy
    print '[INFO] Making the overlay image...'
    num = 1
    total1 = 0
    total2 = 0
    total12 = len(list1) + len(list2) + len(list3)

    def overlay(number, list, list_line):
        global num
        number = str(number)
        os.makedirs(path_result + '/temp' + number)
        for name, name_line in zip(sorted(list), sorted(list_line)):
            img = Image.open(path + '/' + number + '/images/' + name)
            img = img.convert('RGBA')
            img_labels = Image.open(path + '/' + number + '/labels/' + name_line)
            img_new = Image.new("RGBA", img.size)
            img_new.paste(img, (0, 0), img)
            img_new.paste(img_labels, (0, 0), img_labels)
            img_new.save(path_result + '/temp' + number + '/' + name)
            progress = '(' + str(num) + '/' + str(total12) + ')'
            print progress, 'Overlay is completed:', path_result + '/temp' + number + '/' + name
            num += 1

        return None

    overlay(1, list1, list1_line)
    overlay(2, list2, list2_line)
    overlay(3, list3, list3_line)

    # Merge images
    print '\n[INFO] Merging the three images...'
    i = 1
    for name1, name2, name3, name1_fill, name2_fill, name3_fill in zip(sorted(list1), sorted(list2), sorted(list3),
                                                                       sorted(list1_fill), sorted(list2_fill), sorted(list3_fill)):
        img1 = Image.open(path_result + '/temp1/' + name1)
        img2 = Image.open(path_result + '/temp2/' + name2)
        img3 = Image.open(path_result + '/temp3/' + name3)

        # Get dice score
        def getDicescore(first, second):
            first = first.convert("P", palette=Image.WEB)
            first = np.array(first)
            second = second.convert("P", palette=Image.WEB)
            second = np.array(second)
            if len(first) != len(second):
                print '[ERROR] Labels are different.'
                exit(1)
            else:
                if np.array_equal(first, second):
                    ds = float(100.0)
                else:
                    array1_num = 0
                    array2_num = 0
                    array12_num = 0
                    for array1 in first:
                        for i in range(len(first)):
                            if array1[i] != 0:
                                array1_num += 1
                            i += 1
                    for array2 in second:
                        for i in range(len(second)):
                            if array2[i] != 0:
                                array2_num += 1
                            i += 1
                    for array1, array2 in zip(first, second):
                        for i in range(len(array1)):
                            if array1[i] != 0 and array2[i] != 0 and array1[i] == array2[i]:
                                array12_num += 1
                    ds = float(array12_num) / float(array1_num + array2_num - array12_num) * float(100)
                    ds = round(ds, 1)
            return ds

        # Get dice score
        fill1 = Image.open(path + '/1/labels/' + name1_fill)
        fill2 = Image.open(path + '/2/labels/' + name2_fill)
        fill3 = Image.open(path + '/3/labels/' + name3_fill)

        ds12 = getDicescore(fill1, fill2)
        ds13 = getDicescore(fill1, fill3)

        total1 += ds12
        total2 += ds13

        img_width, img_height = img1.size
        img_size = (img_width*3, img_height)
        img_new = Image.new("RGBA", img_size)
        img_new.paste(img1, (0, 0), img1)
        img_new.paste(img2, (img_width, 0), img2)
        img_new.paste(img3, (img_width*2, 0), img3)
        name = name1[:24] + '.png'

        draw = ImageDraw.Draw(img_new)
        font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', 18)
        draw.text((10, 10), 'Normal', font=font, fill=(0, 255, 0))
        draw.text((img_width + 10, 10), 'Fake (Old model)', font=font, fill=(255, 0, 0))
        draw.text((img_width*2 + 10, 10), 'Fake (New model)', font=font, fill=(100, 200, 255))

        draw.text((img_width + 10, img_height - 30), str(ds12) + '%', font=font, fill=(255, 0, 0))
        draw.text((img_width*2 + 10, img_height - 30), str(ds13) + '%', font=font, fill=(100, 200, 255))

        img_new.save(path_result + '/' + name)
        progress = '(' + str(i) + '/' + str(len(list1)) + ')'
        print progress, 'Merging is completed:', path_result + '/' + name
        i += 1

    # Delete temp images
    shutil.rmtree(path_result + '/temp1')
    shutil.rmtree(path_result + '/temp2')
    shutil.rmtree(path_result + '/temp3')
    print '[SUCCESS] Finished all process.'

    # Print result
    print '\n----------------------------------------------------------------------------------------------------' \
          '\nResult' \
          '\n----------------------------------------------------------------------------------------------------' \
          '\nOld model accuracy of an average:', round(total1/float(len(list1)), 2), '%' \
          '\nNew model accuracy of an average:', round(total2/float(len(list1)), 2), '%'

    return None


if __name__ == '__main__':
    main()
