# Following https://www.youtube.com/watch?v=gs0FNQR0njI

import os, shutil

path = r'C:/Users/dovil/Desktop/testinis/'

file_name = os.listdir(path)

folder_names = ['csv files', 'image files', 'text files', 'pdf files']

for name in range(len(folder_names)):
    if not os.path.exists(path + folder_names[name]):
        print(path + folder_names[name])
        os.makedirs((path + folder_names[name]))

file_types = ['.csv', '.png', 'jpeg', '.txt', '.pdf']

for file in file_name:
    if '.csv' in file and not os.path.exists(path + 'csv files/' + file):
        shutil.move(path + file, path + 'csv files/' + file)
    elif '.png' in file and not os.path.exists(path + 'image files/' + file):
        shutil.move(path + file, path + 'image files/' + file)
    elif '.jpeg' in file and not os.path.exists(path + 'image files/' + file):
        shutil.move(path + file, path + 'image files/' + file)
    elif '.txt' in file and not os.path.exists(path + 'text files/' + file):
        shutil.move(path + file, path + 'text files/' + file)
    elif '.pdf' in file and not os.path.exists(path + 'pdf files/' + file):
        shutil.move(path + file, path + 'pdf files/' + file)

print(file_name)
