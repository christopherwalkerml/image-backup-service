from tkinter import *
from PIL import Image, ImageTk
import imagehash, os, cv2, tkinter


img_map = {}
root = Tk()
root.geometry("900x700")
runner = 0

grid = [[None, None]]

def run():
    global runner
    Label(root, text='Choose an image', font=("Ariel", 25)).grid(row=0, column=0, columnspan=2, pady=20)
    
    for folder in ['Iphone 6 - 12-14-2020']:
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

                global_runner = 0
                update_gui(folder, file, data[0], data[1])


def save_vid_as_img(folder, filename):
    vidcap = cv2.VideoCapture(folder + '\\' + filename)
    success,img = vidcap.read()
    cv2.imwrite(folder + '\\' + "temp_frame.jpg", img)


def update_gui(folder_1, file_1, folder_2, file_2):
    img_1 = Image.open(f'{folder_1}\\{file_1}')
    img_2 = Image.open(f'{folder_2}\\{file_2}')
    img_1 = img_1.resize((300, 300))
    img_2 = img_2.resize((300, 300))
    photoimage_1 = ImageTk.PhotoImage(img_1)
    photoimage_2 = ImageTk.PhotoImage(img_2)

    Button(root, image = photoimage_1, command=lambda: del_file(folder_1, file_1)).grid(row=1, column=0, padx=30)
    Button(root, image = photoimage_2, command=lambda: del_file(folder_2, file_2)).grid(row=1, column=1, padx=30)

    Label(root, text=f'{folder_1}\\{file_1}').grid(row=2, column=0)
    Label(root, text=f'{folder_2}\\{file_2}').grid(row=2, column=1)

    while runner == 0:
        root.update()


def del_file(folder, file):
    global runner
    print('deleting ' + folder + '\\' + file)
    runner = 1


def open_tk_img():
    save_vid_as_img(folder, file)
    return Image.open(folder + "\\temp_frame.jpg")

run()