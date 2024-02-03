
import matplotlib.pyplot as plt
import cv2
import colorsys
import numpy as np
import xml.etree.ElementTree as ET
from xml.dom import minidom
import math
import xml
import os
from bs4 import BeautifulSoup
from tkinter import filedialog


def sub_plots( images , figsize = (16 , 9) , labels= [] , save_fig = False , save_plot_to = None, show_plot = True):
    
    """
    Create subplots of images with labels.

    Parameters:
        images (np.ndarray): Array of images.
        figsize (tuple): Figure size (width, height).
        labels (list): List of labels for images.
        save_fig (bool): Flag to save the figure.
        save_plot_to (str): Directory to save the plot.
        show_plot (bool): Flag to display the plot.

    Returns:
        None
    """

    data_shape = np.array(images).shape
 
    if data_shape[0] < 3 and len(data_shape) > 3:
        for image in images:
            plt.figure()
            plt.imshow(image)
            plt.show()
            
    elif data_shape[0] >= 3 and int(len(data_shape)) > 3:  
        
          
        num_columns = math.ceil((math.sqrt(len(images))))
        num_rows = math.ceil(len(images) / num_columns)
        num_images = len(images)
        # num_columns = 8
        # num_rows = math.ceil(num_images/num_columns) +1
        
        fig, axs = plt.subplots(num_rows, num_columns, figsize=figsize)
        for i in range(num_rows):
            for j in range(num_columns):
                index = i * num_columns + j
                
                if index < num_images:
                    if len(labels) > 0:
                        axs[i, j].set_title(labels[index])
                    axs[i, j].imshow(images[index])  # Replace this with your actual image data
                    axs[i, j].axis('off')  # Turn off axis labels
                else:
                    axs[i, j].axis('off')  # Turn off axis labels for empty subplots

    
        plt.tight_layout()
        if save_fig:
            if save_plot_to == None:
                path = os.path.join(os.getcwd() , "output.png")
            else:
                path = (os.path.join(save_plot_to , "output.png"))
            print(f"File saved in {path}")
            plt.savefig(path)
            
        # Display the figure
        if show_plot:
            plt.show()
    
    else:
       print("INvalid data structure Expected (None , 320 , 320 , 3)")



def test_color_box(class_color_dict , plot = True):
    """
    Expected input {label :{name :Color_box}}
    
    Output return images , labels
    """
    images = []
    labels = []
    for class_label, color in class_color_dict.items():
       
        name, color = list(color.items())[0]
        many = [color for i in range(125)]
        image =np.array([many for i in range(150)])
        extra_info = class_label , name
        
        images.append(image)
        labels.append(extra_info)
        
    images = np.array(images) 
    images , labels
    if plot:
        sub_plots(images=images , labels=labels) 
    return images , labels
    

def generate_distinct_colors(num_classes):
    # Generate distinct RGB colors using evenly spaced hues in HSV color space
    hues = np.linspace(0, 1, num_classes)
    hsv_colors = np.column_stack((hues, np.full_like(hues, 1.0), np.full_like(hues, 0.85)))
    rgb_colors = (np.array([colorsys.hsv_to_rgb(*hsv) for hsv in hsv_colors]) * 255).astype(int)
    return rgb_colors.tolist()

def create_class_color_dict(class_names):
    """
    Iinput = list of clas names
    output {label :{name: color box}}
    """
    num_classes = int(len(class_names))
    colors = generate_distinct_colors(num_classes)
    class_color_dict = {i: {class_names[i ]:colors[i]} for i in range(num_classes)}
    return class_color_dict


def draw_single_box(image, boxes,current_class,  class_colors , ready_cordinates = False , put_text = False , score= 0.00) :
    
    
    """
    Draw a single bounding box on an image.

    Parameters:
        - image (numpy.ndarray): The input image.
        - boxes (tuple): Coordinates of the bounding box in the format (ymin, xmin, ymax, xmax).
        - current_class: The class label or name associated with the object.
        - class_colors (dict): Dictionary mapping class indices to colors.
        - ready_cordinates (bool): If True, assumes the provided coordinates are ready to use. If False, normalizes the coordinates.
        - put_text (bool): If True, puts the object label text on the image.
        - score (float): The confidence score associated with the detection.

    Returns:
        numpy.ndarray: Image with the bounding box drawn.
    """
    
    imH, imW, _ = image.shape

    object_color = (list(class_colors[int(current_class)].items())[0])[1]

    if type(current_class) is int:
        object_name = (list(class_colors[int(current_class)].items())[0])[0]
    else:
        object_name = str(current_class)
    # Get bounding box coordinates and draw box
    # Interpreter can return coordinates that are outside of image dimensions, need to force them to be within image using max() and min()
    if not ready_cordinates:
        ymin = int(max(1,(boxes[1] * imH)))
        xmin = int(max(1,(boxes[0] * imW)))
        ymax = int(min(imH,(boxes[3] * imH)))
        xmax = int(min(imW,(boxes[2] * imW)))
    elif ready_cordinates:
        ymin= int(float(boxes[1]))
        xmin= int(float(boxes[0]))
        ymax = int(float(boxes[3]))
        xmax= int(float(boxes[2]))

   
    cv2.rectangle(image, (xmin,ymin), (xmax,ymax), object_color, 2)
    
    
    if put_text:
        cv2.putText(image, object_name, (xmin, ymin - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 210, 0), 2)
    return image



def draw_from_xml(image,image_shape , cordinates , object_colors):
    
    for i in range(len(cordinates)):
        object_color = object_colors[i]
        
        cordinate = np.array(cordinates[i]).astype(np.float32)
       
        image_height , image_width = image_shape
        image_height = int(image_height)
        image_width = int(image_width)
      
        ymin = int(max(1,(cordinate[0] * image_height )))
        xmin = int(max(1,(cordinate[1] * image_width)))
        ymax = int(min(image_height,(cordinate[2] * image_height)))
        xmax = int(min(image_height,(cordinate[3] * image_width)))
    
        
        cv2.rectangle(image, (xmin,ymin), (xmax,ymax), object_color, 2)
    return image
    

def get_folder_gui(initial_dir):
    folder = filedialog.askdirectory(initialdir=initial_dir)
    return folder


def parse_xml(xml_path):
    """
    Parse an XML file containing image annotations.

    Parameters:
        xml_path (str): Path to the XML file.

    Returns:
        dict or None: Parsed data in the format {image_paths:  [ ....[label,object_name , accuracy , list(cordinates)]....,] } or None if the file doesn't exist.

    XML Format:
        - The XML file should have a root element with ImagePath tags.
        - Each ImagePath tag should contain a Path subtag with the image path.
        - Within each ImagePath tag, there should be Object tags with Label, Name, Score, y_min, x_min, y_max, x_max subtags for each detected object.
        - The function extracts image paths, sizes, and object details from these tags.

    Example XML Structure:
        <Annotations>
            <Image>
                <Path>/path/to/image1.jpg</Path>
                <Object>
                    <Label>1</Label>
                    <Name>object1</Name>
                    <Score>0.95</Score>
                    <y_min>0.1</y_min>
                    <x_min>0.2</x_min>
                    <y_max>0.8</y_max>
                    <x_max>0.9</x_max>
                </Object>
                <!-- Additional Object tags for other detected objects -->
            </Image>
            <!-- Additional ImagePath tags for other images -->
        </Annotations>
    """
  
    xml_file_path = xml_path
    
    if not os.path.isfile(xml_file_path):
        return None
    
    
    tree = ET.parse(xml_file_path)
    root = tree.getroot()
    # Convert the XML tree to a string
    xml_string = ET.tostring(root, encoding='utf8').decode('utf8')
    
    # Prettify the XML string using xml.dom.minidom
    xml_prettified = xml.dom.minidom.parseString(xml_string).toprettyxml()


    # Parse the string with BeautifulSoup
    soup = BeautifulSoup(xml_prettified, 'xml')

    # Find all 'ImagePath' tags
    image_paths = soup.find_all('Image')
    
    final_data = {}
    
    found_images_paths = []
    for i in image_paths:
    
        #get image path
        image_path = i.find("Path").text.strip()
        
        if image_path not in found_images_paths:
            
            final_data[image_path] = []
            found_images_paths.append(image_path)


        multiple_detections = i.find_all("Object")
        
        #track detetcted objects per image
        detected_cords_per_image = []

        found = []
        for j in multiple_detections:
            
            label = j.find("Label").text.strip("\n")
            object_name = j.find("Name").text.strip('\n')
            accuracy = float(j.find("Score").text.strip())
            cordinates = float(j.find("x_min").text.strip() ), float(j.find("y_min").text.strip()) , float(j.find("x_max").text.strip()) ,float(j.find("y_max").text.strip())

            data = [int(float(label)),object_name , accuracy , list(cordinates)]
            
          
            
            if data not in found:
                detected_cords_per_image.append(data)
                found.append(data)
        
        final_data[image_path]=detected_cords_per_image 

    return  final_data



