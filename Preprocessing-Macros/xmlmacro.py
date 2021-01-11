import os
from xml.etree import ElementTree
filedest = ""


"""
Change the elements inside the xml file to custom label.
"""

for filename in os.listdir(filedest):
    if filename[-4:] == ".xml":
        load = filedest + filename
        tree = et.parse(load)
        root = tree.getroot()
        tree.find('.//name').text = 'license'
        tree.write(load)



