from PIL import Image
import os
delete = []
path = #PATH
for file in os.listdir(path):
     extension = file.split('.')[-1]
     if extension == 'PNG':
           fileLoc = path+file
           img = Image.open(fileLoc)
           if img.mode != 'RGB' and img.mode!= 'RGBA':
                 print(file[0:-4])
                 delete.append(file[0:-4])

     if extension == 'jpg':
           fileLoc = path+file
           img = Image.open(fileLoc)
           if img.mode != 'RGB' and img.mode!= 'RGBA':
                 print(file[0:-4])
                 delete.append(file[0:-4])

     if extension == 'jpeg':
           fileLoc = path+file
           img = Image.open(fileLoc)
           if img.mode != 'RGB' and img.mode!= 'RGBA':
                 print(file[0:-4])
                 delete.append(file[0:-4])

     if extension == 'png':
           fileLoc = path+file
           img = Image.open(fileLoc)
           if img.mode != 'RGB' and img.mode!= 'RGBA':
                 print(file[0:-4])
                 delete.append(file[0:-4])

for file in delete:
    os.remove(path+file+".PNG")
    os.remove(path+file+".xml")