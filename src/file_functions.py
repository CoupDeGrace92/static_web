import os
import shutil

def move_to_clean(target, destination, logging=False):
    if not os.path.exists(target):
        print(f'File/directory to copy - {target} - not found')
        return
    if os.path.exists(destination):
        if logging:
            print(f'Directory {destination} exists - cleaning directory')
        shutil.rmtree(destination)
        if logging:
            print(f'Directory {destination} removed - creating empty directory')
        os.mkdir(destination)
        if logging:
            print(f'Directory {destination} empty and ready for copying')
    else:
        os.mkdir(destination)
        if logging:
            print(f'Directory {destination} not found')
            print(f'Creating {destination}')
    dir_move(target, destination, logging)

def dir_move(target, destination, logging=False):
    for i in os.listdir(target):
        appended_location = os.path.join(target, i)
        if os.path.isdir(appended_location):
            appended_destination = os.path.join(destination, i) 
            print(f'Creating folder: {appended_destination}')
            os.mkdir(appended_destination)
            dir_move(appended_location, appended_destination)
        else:
            if not os.path.isfile(appended_location):
                if logging:
                    print(f'Attempted to copy object {i} as a file - object {i} is not a file')
                raise Exception(f'Object {i} is not a file')
            appended_destination = os.path.join(destination, i)
            if logging:
                print(f'Copying {i} to {appended_destination}')
            shutil.copy(appended_location, appended_destination) #Habit in formatting from os - shutil allows us to use the destination file and will create a file with the same name
    if logging:
        print('All files copied')
