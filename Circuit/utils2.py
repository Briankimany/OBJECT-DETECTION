import  xml.etree.ElementTree as ET
from xml.dom import minidom
import numpy as np
import os , json
import glob
import cv2
import matplotlib.pyplot as plt
from utils import parse_xml , create_class_color_dict , draw_single_box
from PIL import Image
import random
import tkinter as tk
from tkinter import filedialog


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def read_image(image_path , shape= (300 , 300) , batch_loading = False , bgr_ready = False):
    """
    Load and preprocess images using OpenCV , range =  [0 , 1]

    Parameters:
        - image_path: Path to the image file.
        - shape: Tuple (width, height) specifying the target size.
        - batch_loading: If True, return images without batch dimension.
        - bgr_ready: If True, assume the input image is in BGR format.

    Returns:
        - input_data: Processed image data.
            - If batch_loading is False, shape is (1, width, height, 3).
            - If batch_loading is True, shape is (width, height, 3).
    """
    
    image = cv2.imread(image_path)
    # print(image.shape)
    if  not bgr_ready:
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    else:
        image_rgb = image
        

    width, height = shape
    image_resized = cv2.resize(image_rgb, (width, height))
    image_resized  = np.array(image_resized) / 255.0
    
    if not batch_loading:
        input_data = np.expand_dims(image_resized, axis=0)
    else:
        input_data = image_resized
    
    return input_data


def save_dict_to_xml(data , folder = None , ready_file = False):

    """
    Save detection results in XML format.

    Parameters:
        - data (dict): Detection results in the format {image_path: [detections]}.
        - folder (str): Optional folder path for saving XML files.
        - ready_file (bool): If True, assume the XML file is already prepared.

    Returns:
        None
 
    Input ==  {
             File_name_1:[... , [label, object_name, score , "(x_min ,y_min , x_max , y_max)"] , ...  ] , 
             File_name_2:[.. , [label, "object_name", score, "(x_min ,y_min , x_max , y_max)"] , ...  ],
             }
    """
    
    root = ET.Element("Annotations")
    
    for file in data:
        
        file_annots = ET.SubElement(root  , "Image")
        path_annots = ET.SubElement(file_annots , "Path") 
        path_annots.text = str(file)
        
        detections = data[file]
        
        for detection in detections:

            detection_annot = ET.SubElement(file_annots , 'Object')
            
            label , object_detected , score , cordinates = detection
               
               
            if not isinstance(cordinates , (list , tuple )):
                cordinates = cordinates.replace('[' , '' )
                cordinates = cordinates.replace(']' , '' )
                cordinates = cordinates.split(" ")
                cordinates = [i.strip() for i in cordinates if len(i) > 0]
                print(cordinates)
                
            label_annot = ET.SubElement(detection_annot ,'Label')
            object_annot = ET.SubElement(detection_annot , "Name")
            score_annot = ET.SubElement(detection_annot ,'Score')
            
            label_annot.text = str(label)
            object_annot.text = object_detected
            score_annot.text = str(score)
            
            x_min ,y_min  , x_max , y_max = cordinates
            
            cordinate_annots = ET.SubElement(detection_annot , "Cordinates")
            
            Y_min_annot = ET.SubElement(cordinate_annots , 'y_min')
            X_min_annot = ET.SubElement(cordinate_annots , 'x_min')
            Y_max_annot = ET.SubElement(cordinate_annots , 'y_max')
            X_max_annot = ET.SubElement(cordinate_annots , 'x_max')
            
            Y_min_annot.text = str(y_min)
            X_min_annot.text = str(x_min)
            Y_max_annot.text = str(y_max)
            X_max_annot.text = str(x_max)
            
        ET.SubElement(root , "Next")
            

    xml_string = ET.tostring(root, encoding='utf-8')
    parsed_string = minidom.parseString(xml_string)
    pretty_xml = parsed_string.toprettyxml(indent="  ")
    
    xml_path = folder
    
    if folder == None:
        xml_path = 'detections.xml'
    else:
        name , ext = os.path.splitext(folder)
        
        if len(ext) > 0:
            os.makedirs(os.path.dirname(folder) , exist_ok=True)
            xml_path = folder
        
        else:
            os.makedirs(folder , exist_ok=True)
            xml_path = os.path.join(folder , "detections.xml")            
    
    with open(xml_path, 'w') as file:
        file.write(pretty_xml)
        

def grab_image_from_dir(imgpath="images", labelpath = '', modelpath = '' , num_test_images= 5 , only_images = False , select_random= True) :
    """
    Grab images and labels from a directory.

    Parameters:
        - imgpath (str): Path to the image folder or file.
        - labelpath (str): Path to the label file.
        - modelpath (str): Path to the model file.
        - num_test_images (int): Number of test images to grab.
        - only_images (bool): If True, return only images.
        - select_random (bool): If True, select images randomly.

    Returns:
        tuple: Tuple containing images and labels.
    """
    
    
    # Grab filenames of all images in test folder
    if os.path.isdir(imgpath):
        images = glob.glob(imgpath + '/*.jpg') + glob.glob(imgpath + '/*.JPG') + glob.glob(imgpath + '/*.png') + glob.glob(imgpath + '/*.bmp') +  glob.glob(imgpath + '/*.jpeg')
    else:
        if os.path.isfile(imgpath) and num_test_images == 1 :
            images = [imgpath] 
        else:
            # images = os.listdir(os.path.dirname(imgpath))
            imgpath = os.path.dirname(imgpath)
            images = glob.glob(imgpath + '/*.jpg') + glob.glob(imgpath + '/*.JPG') + glob.glob(imgpath + '/*.png') + glob.glob(imgpath + '/*.bmp')

    
    if select_random:
        
        if len (images)  > num_test_images:
            images = random.sample(images, num_test_images)
        else:
            print("Bringing all images")
            images = images
    
    if only_images :
        return images , None
    
    
    # Load the label map into memory
    labels= []
    if os.path.exists(labelpath):
            
            with open(labelpath, 'r') as f:
                    cont = f.readlines()
            
            for name in cont:
                labels.append(name.strip())
                
    elif os.path.exists(modelpath):
            dir_name = os.path.dirname(modelpath)
            
            for file in os.listdir(dir_name):
                file_name , ext = os.path.splitext(file)
                file_name = file_name.lower()

                if "name" in file_name or "label" in file_name and ext == ".txt":
                    labelpath= os.path.join(dir_name , file)
                    labels= []
                    with open(labelpath, 'r') as f:
                            cont = f.readlines()
                    
                    for name in cont:
                        if len(name) > 1:
                            labels.append(name.strip())
                        
    else:
        print("Invalid labels path")
        
        with open(read_path(os.getcwd()) , 'r') as file:
            cont = file.readlines()
            
            labels = [word.strip() for word in cont if len(word) > 1]
            

            

    if len(labels) < 1:
        labels = None            
    return images , labels
  
  
def join_break_xml(xml_paths ,task ="b"):    
    """
    Perform either joining ('j') or breaking ('b') of XML data.

    Parameters:
    - xml_paths: List of XML file paths.
    - task: 'j' for joining, 'b' for breaking.

    Returns:
    - If task is 'j', returns a dictionary.
    - If task is 'b', returns a list of dictionaries.
    """

    
    if task.lower() == 'j':
        dict_list = list(map(parse_xml , xml_paths))

        parent_list = []

        for dict_ in dict_list:
            
            parent_list += list(dict_.items())
            
        return  dict(parent_list)

    elif task.lower() == 'b':
        
        big_dicts = list(map(parse_xml , xml_paths))
        
        def break_dict(dictionary):
            return [ {name:dictionary[name]} for name in dictionary ] 
        
        broken_dicitionaries = list(map (break_dict , big_dicts))
        
        return broken_dicitionaries
    
    else:
        print("Uknown task" ,task)
        return None
        

def visualize_dict(data , count = {}, show_names= False):
    
    """
    Visualizes dict data by drawing bounding boxes on corresponding images.

    Parameters:
    - data (dict): A dictionary containing image paths as keys and a list of bounding box information as values.
    - count (dict, optional): A dictionary to keep track of the count for each class. Defaults to an empty dictionary.

    Returns:
    - np.ndarray: An array of images with bounding boxes drawn on them.


    data =  {
             File_name_1:[... , [label, object_name, score , "(y_min ,x_min , y_max , x_min)"] , ...  ] , 
             File_name_2:[.. , [label, "object_name", score, "(y_min ,x_min , y_max , x_min)"] , ...  ],
             }

    result = Visualize_xml(data)

    """
    
    with open ("dict.json" , 'r') as file:
        names_dict = json.load(file)
    print("listing in" , os.getcwd())
    data = list(zip(list(data.keys()) , list(data.values())))

    names =list(names_dict.values())

    class_color_dict = create_class_color_dict(names)
    final_data = []
    def draw(data_ ,class_color_dict = class_color_dict , show_names = show_names):
        image_p  , cords = data_
        image = Image.open(image_p)
        image = image.resize((320 , 320))
        image = np.array(image)

        for cord in cords:
            lab_ , _ , _ , points = cord
            if names[int(lab_)] not in  count:
                count[names[int(lab_)]] = 1
            else:
                count[names[int(lab_)]] +=1
            
            boxesa = [int(float(i)) for i in points]
            
            image =  draw_single_box( image= image, boxes = boxesa,current_class= int(float(lab_)) , class_colors=class_color_dict , ready_cordinates= True , put_text=show_names )
        
        return image
    
    
    final_data = list(map(draw ,data ))
        
    return np.array(final_data)

def read_path(directory):
    try:
        root = tk.Tk()
        root.withdraw()
        
        root.configure(bg='purple')
        root.geometry('800x600')

        file_path = filedialog.askopenfilename(filetypes=[("All Files", "*.*")], initialdir=directory, title=directory)

        root.destroy()
        return file_path

    except KeyboardInterrupt:
        print("good bye")


    
