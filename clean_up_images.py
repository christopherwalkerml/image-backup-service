from tkinter import *
from PIL import Image, ImageTk
import imagehash, os, cv2
from tkinter import filedialog


img_map = {}
root = Tk()
root.geometry("600x160")
runner = 0
merge_folder = ""
other_folder = ""
    

def run():
    global runner

    Label(root, text="choose folder to merge into: ").grid(row=0, column=0)
    Button(root, text="Choose", command=get_merge_directory).grid(row=1, column=0)
    Label(root, text="choose folder to get images from: ").grid(row=2, column=0)
    Button(root, text="Choose", command=get_other_directory).grid(row=3, column=0)
    Button(root, text="Continue", command=start_program).grid(row=4, column=0, pady=30)

    while not runner:
        root.update()

    root.grid_remove()

    root.geometry("1140x700")
    
    Label(root, text='Choose an image to keep', font=("Ariel", 25)).grid(row=0, column=0, columnspan=2, pady=20)
    
    for folder in [merge_folder, other_folder]:
        print(folder)
        for file in os.listdir(folder):
            print(file)
            if file == "temp_frame.jpg":
                continue
            
            if '.aae' in file.lower():
                os.remove(os.path.dirname(os.path.realpath(__file__)) + '\\' +  folder + '\\' + file)
                
            if '.mov' in file.lower() or '.mp4' in file.lower():
                save_vid_as_img(folder, file)
                hashed = imagehash.average_hash(Image.open(folder + "\\temp_frame.jpg"))
            else:
                hashed = imagehash.average_hash(Image.open(folder + '\\' + file))
                
            if hashed not in img_map:
                img_map[hashed] = [folder, file]
            else:
                data = img_map[hashed]
                print(folder + '\\' + file + '  ==  ' + data[0] + '\\' + data[1])

                runner = 0
                update_gui(folder, file, data[0], data[1])


def save_vid_as_img(folder, filename):
    vidcap = cv2.VideoCapture(folder + '\\' + filename)
    success,img = vidcap.read()
    cv2.imwrite(folder + '\\' + "temp_frame.jpg", img)


def update_gui(folder_1, file_1, folder_2, file_2):
    img_1 = open_tk_img(folder_1, file_1)
    img_2 = open_tk_img(folder_2, file_2)

    Button(root, image = img_1, command=lambda: del_file(folder_1, file_1)).grid(row=1, column=0, padx=30)
    Button(root, image = img_2, command=lambda: del_file(folder_2, file_2)).grid(row=1, column=1, padx=30)

    Label(root, text=f'{folder_1}\\{file_1}').grid(row=2, column=0, pady=20)
    Label(root, text=f'{folder_2}\\{file_2}').grid(row=2, column=1, pady=20)

    Button(root, text="Keep Both", command=lambda: reset_runner()).grid(row=3, column=0, columnspan=2)

    while runner == 0:
        root.update()


def del_file(folder, file):
    global runner
    print('deleting ' + folder + '\\' + file)
    runner = 1


def reset_runner():
    global runner
    runner = 1


def open_tk_img(folder, file):
    if '.mov' in file.lower() or '.mp4' in file.lower():
        save_vid_as_img(folder, file)
        img = Image.open(folder + "\\temp_frame.jpg")
    else:
        img = Image.open(f'{folder}\\{file}')
        
    img = img.resize((500, 500))
    return ImageTk.PhotoImage(img)


def get_merge_directory():
    global merge_folder
    merge_folder = filedialog.askdirectory()
    Label(root, text=f'({merge_folder})').grid(row=1, column=1)

def get_other_directory():
    global other_folder, runner
    other_folder = filedialog.askdirectory()
    Label(root, text=f'({other_folder})').grid(row=3, column=1)


def start_program():
    runner = 1
    
    
run()
