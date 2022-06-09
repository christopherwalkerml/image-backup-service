from tkinter import *
from PIL import Image, ImageTk
import imagehash, os, cv2, random, shutil, json
from tkinter import filedialog


img_map = {}
keep = {}
root = Tk()
root.geometry("600x160")
frame = Frame(root)
runner = 0
merge_folder = ""
other_folder = ""
    

def run():
    global runner, keep

    Label(frame, text="choose folder to merge into: ").grid(row=0, column=0)
    Button(frame, text="Choose", command=get_merge_directory).grid(row=1, column=0)
    Label(frame, text="choose folder to get images from: ").grid(row=2, column=0)
    Button(frame, text="Choose", command=get_other_directory).grid(row=3, column=0)
    Button(frame, text="Continue", command=start_program).grid(row=4, column=0, pady=30)
    frame.grid()

    while not runner:
        root.update()

    frame.destroy()

    root.geometry("1140x750")
    
    Label(root, text='Choose an image to keep', font=("Ariel", 25)).grid(row=0, column=0, columnspan=2, pady=20)
    directory_label = Label(root, text='/', font=("Ariel", 16))
    directory_label.grid(row=1, column=0, columnspan=2, pady=10)

    if os.path.isfile('saved_keeps.json'):
        with open('saved_keeps.json', 'r') as f:
            keep = json.load(f)
    
    for folder in [merge_folder, other_folder]:
        for file in os.listdir(folder):
            directory_label.destroy()
            directory_label = Label(root, text=f'{folder}/{file}', font=("Ariel", 16))
            directory_label.grid(row=1, column=0, columnspan=2, pady=10)
            
            root.update()
                  
            if file == "temp_frame.jpg":
                continue
            
            if '.aae' in file.lower():
                os.remove(f'{folder}/{file}')
                continue
                
            if '.mov' in file.lower() or '.mp4' in file.lower():
                save_vid_as_img(folder, file)
                hashed = imagehash.average_hash(Image.open('temp_frame.jpg'))
            else:
                hashed = imagehash.average_hash(Image.open(f'{folder}/{file}'))
                
            if hashed not in img_map:
                # if the file needs to be merged into the merge folder
                if folder != merge_folder:
                    # get the new file name and add it to the has list
                    fpath = move_file(folder, file)
                    img_map[hashed] = [merge_folder, os.path.basename(fpath)]
                else:
                    # else, add the regular file to the has list since it's not moving
                    img_map[hashed] = [merge_folder, file]
                    
            else:
                data = img_map[hashed]

                if check_for_keep(folder, file, data[0], data[1]):
                    continue

                runner = 0
                update_gui(folder, file, data[0], data[1], hashed)

            if keep:
                with open('saved_keeps.json', 'w+') as f:
                    f.write(json.dumps(keep))


def save_vid_as_img(folder, filename):
    vidcap = cv2.VideoCapture(f'{folder}/{filename}')
    success,img = vidcap.read()
    cv2.imwrite("temp_frame.jpg", img)


def update_gui(folder_1, file_1, folder_2, file_2, hashval):
    img_1 = open_tk_img(folder_1, file_1)
    img_2 = open_tk_img(folder_2, file_2)

    Button(root, image = img_1, command=lambda: merge_file(folder_2, file_2, folder_1, file_1, hashval)).grid(row=2, column=0, padx=30)
    Button(root, image = img_2, command=lambda: merge_file(folder_1, file_1, folder_2, file_2, hashval)).grid(row=2, column=1, padx=30)

    l1 = Label(root, text=f'{folder_1}/{file_1}')
    l1.grid(row=3, column=0, pady=20)
    l2 = Label(root, text=f'{folder_2}/{file_2}')
    l2.grid(row=3, column=1, pady=20)

    Button(root, text="Keep Both", command=lambda: keep_both(folder_1, file_1, folder_2, file_2)).grid(row=4, column=0, columnspan=2)

    while runner == 0:
        root.update()
    l1.destroy()
    l2.destroy()


def merge_file(del_folder, del_file, keep_folder, keep_file, hashval):
    global runner
    
    os.remove(f'{del_folder}/{del_file}')
    # if deleting the local file, move the external file to the local folder
    if del_folder == merge_folder:
        fpath = move_file(keep_folder, keep_file)
        img_map[hashval] = [os.path.dirname(fpath), os.path.basename(fpath)]

    runner = 1


def move_file(old_folder, old_file):
    global runner
    
    name = ''.join([str(random.randrange(10)) for x in range(16)])
    while os.path.exists(f'{merge_folder}/{name}'):
        name = ''.join([str(random.randrange(10)) for c in range(16)])

    file, ext = os.path.splitext(old_file)
    shutil.move(f'{old_folder}/{old_file}', f'{merge_folder}/{name}{ext}')
    return f'{merge_folder}/{name}{ext}'


def keep_both(folder_1, file_1, folder_2, file_2):
    global runner
    runner = 1

    if folder_1 != merge_folder:
        f1 = move_file(folder_1, file_1)
    else:
        f1 = f'{folder_1}/{file_1}'
    if folder_2 != merge_folder:
        f2 = move_file(folder_2, file_2)
    else:
        f2 = f'{folder_2}/{file_2}'

    if f1 not in keep:
        keep[f1] = []
    keep[f1].append(f2)
    if f2 not in keep:
        keep[f2] = []
    keep[f2].append(f1)
        

def open_tk_img(folder, file):
    if '.mov' in file.lower() or '.mp4' in file.lower():
        save_vid_as_img(folder, file)
        img = Image.open('temp_frame.jpg')
    else:
        img = Image.open(f'{folder}/{file}')
        
    img = img.resize((500, 500))
    return ImageTk.PhotoImage(img)


def get_merge_directory():
    global merge_folder
    merge_folder = filedialog.askdirectory()
    Label(frame, text=f'({merge_folder})').grid(row=1, column=1)

def get_other_directory():
    global other_folder, runner
    other_folder = filedialog.askdirectory()
    Label(frame, text=f'({other_folder})').grid(row=3, column=1)


def start_program():
    global runner
    runner = 1


def check_for_keep(folder_1, file_1, folder_2, file_2):
    if f'{folder_1}/{file_1}' not in keep:
        return False

    if f'{folder_2}/{file_2}' not in keep[f'{folder_1}/{file_1}']:
        return False

    del keep[f'{folder_1}/{file_1}']
    del keep[f'{folder_2}/{file_2}']

    keep_both(folder_1, file_1, folder_2, file_2)
    
    return True
    
    
run()
