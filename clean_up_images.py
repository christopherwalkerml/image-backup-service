from tkinter import *
from PIL import Image, ImageTk
import imagehash, os, cv2, random
from tkinter import filedialog


img_map = {}
root = Tk()
root.geometry("600x160")
frame = Frame(root)
runner = 0
merge_folder = ""
other_folder = ""
    

def run():
    global runner

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
    directory_label = Label(root, text='\\', font=("Ariel", 16))
    directory_label.grid(row=1, column=0, columnspan=2, pady=10)
    
    for folder in [merge_folder, other_folder]:
        for file in os.listdir(folder):
            directory_label.destroy()
            directory_label = Label(root, text=f'{folder}/{file}', font=("Ariel", 16))
            directory_label.grid(row=1, column=0, columnspan=2, pady=10)
            
            root.update()
                  
            if file == "temp_frame.jpg":
                continue
            
            if '.aae' in file.lower():
                os.remove(f'{folder}\{file}')
                
            if '.mov' in file.lower() or '.mp4' in file.lower():
                save_vid_as_img(folder, file)
                hashed = imagehash.average_hash(Image.open(f'{folder}\{temp_frame.jpg}'))
            else:
                hashed = imagehash.average_hash(Image.open(f'{folder}\{file}'))
                
            if hashed not in img_map:
                img_map[hashed] = [folder, file]

                if folder != merge_folder:
                    merge_file(folder, file, merge_folder)
            else:
                data = img_map[hashed]

                runner = 0
                update_gui(folder, file, data[0], data[1])


def save_vid_as_img(folder, filename):
    vidcap = cv2.VideoCapture(folder + '\\' + filename)
    success,img = vidcap.read()
    cv2.imwrite(folder + '\\' + "temp_frame.jpg", img)


def update_gui(folder_1, file_1, folder_2, file_2):
    img_1 = open_tk_img(folder_1, file_1)
    img_2 = open_tk_img(folder_2, file_2)

    Button(root, image = img_1, command=lambda: del_file(folder_2, file_2, folder_1, file_1)).grid(row=2, column=0, padx=30)
    Button(root, image = img_2, command=lambda: del_file(folder_1, file_1, folder_2, file_2)).grid(row=2, column=1, padx=30)

    l1 = Label(root, text=f'{folder_1}/{file_1}')
    l1.grid(row=3, column=0, pady=20)
    l2 = Label(root, text=f'{folder_2}/{file_2}')
    l2.grid(row=3, column=1, pady=20)

    Button(root, text="Keep Both", command=lambda: reset_runner()).grid(row=4, column=0, columnspan=2)

    while runner == 0:
        root.update()
    l1.destroy()
    l2.destroy()


def del_file(del_folder, del_file, keep_folder, keep_file):
    global runner
    
    os.remove(f'{del_folder}\{del_file}')
    if del_folder == merge_folder:
        merge_file(keep_folder, keep_file, del_folder)

    runner = 1


def merge_file(old_folder, old_file, folder):
    name = ''.join([str(random.randrange(10)) for x in range(16)]) + '.jpg'
    while os.path.exists(f'{folder}\{name}'):
        name = ''.join([str(random.randrange(10)) for c in range(16)]) + '.jpg'

    Image.open(f'{old_folder}\{old_file}').save(f'{folder}\{name}', 'PNG')


def reset_runner():
    global runner
    runner = 1


def open_tk_img(folder, file):
    if '.mov' in file.lower() or '.mp4' in file.lower():
        save_vid_as_img(folder, file)
        img = Image.open(f'{folder}\temp_frame.jpg')
    else:
        img = Image.open(f'{folder}\{file}')
        
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
    
    
run()
