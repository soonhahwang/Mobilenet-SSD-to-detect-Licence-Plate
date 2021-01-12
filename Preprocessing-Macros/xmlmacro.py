import os
from xml.etree import ElementTree as et
from xml.dom import minidom
from shutil import copyfile

"""
Change the elements inside the xml file to custom label.
"""

img = ""
xml = ""
# #Macro for changing xml
# for filename in os.listdir(filedest):
#     if filename[-4:] == ".xml":
#         load = filedest + filename
#         tree = et.parse(load)
#         root = tree.getroot()
#         tree.find('.//name').text = 'license'
#         tree.write(load)

##Macro for creating xml
# open("xml"+"temp.xml", "w+")
# copyfile(xml+"01-A-2808.xml", xml+"test.xml")
count = 0
for filename in os.listdir(img):
    tempname = filename[0:-4]
    tempname = tempname + ".xml"
    print(tempname)

    open("xml"+tempname, "w+")
    copyfile(xml + "test.xml", xml+tempname)

    tree = et.parse(xml+tempname)
    root = tree.getroot()
    tree.find('.//filename').text = filename
    tree.write(xml+tempname)


