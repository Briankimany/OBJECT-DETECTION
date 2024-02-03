
from ultralytics import YOLO
from PIL import Image
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import json


from utils import sub_plots, create_class_color_dict  , get_folder_gui , draw_single_box
from utils2 import save_dict_to_xml, grab_image_from_dir  , clear_console

class YOLOModel():
    
    def __init__(self, image_path=None, output_dir=None,  num_images=5, min_conf=0.7 , show_single = False , save_images = False):
        """
        Initialize the YOLOModel object.

        Args:
            output_dir (str): Directory to save output files.
            image_dir (str): Directory containing input images for detection.
            num_images (int): Number of images to process for detection.
            min_conf (float): Minimum confidence level for object detection.
        """
        
        self.output_dir = output_dir
        self.image_dir_source = image_path
        self.num_images = num_images
        self.min_conf = min_conf
        self.new_data_structure = None
        self.processed_data = None
        self.images_paths = None
        self.model = YOLO("best.pt")
        self.final_data = None
        self.show_single = show_single
        self.save_images = save_images
        self.names = None
        self.show_images_text = False
        

    def process_images(self , images_list = None):
        
        if images_list != None:
            self.image_dir_source = images_list
        
        self.images_paths = grab_image_from_dir(self.image_dir_source, only_images=True , num_test_images= self.num_images)[0]
        
        if hasattr(self, 'proccesed_images') and self.proccesed_images is not None:
            
            del self.proccesed_images
        self.proccesed_images = None
        
        def read_image(image_path):
            image = Image.open(image_path)
            image = image.resize((320 , 320))
            return np.array(image)
        
        self.proccesed_images = np.array(list(map(read_image ,  self.images_paths)))
     
    def predict(self):
        
        def pred(image):
            return self.model.predict(image, conf = self.min_conf)
        
        self.results  = list(map(pred , self.proccesed_images))
    

        new_data_sructure = {}
        for i ,res in enumerate(self.results):
            
            res =res[0]
             
            detections_per_image = []
            image_detections  = res.boxes.data
            
            for object_detected in image_detections:
                
                object_detected = [float(i) for i in object_detected]
                xmin , ymin , xmax , ymax  , score , class_label= object_detected
                object_name = res.names[int(class_label)]
                
                data = [class_label , object_name , score , (xmin ,ymin , xmax , ymax)]
                
                detections_per_image.append(data)
                
            image_path = self.images_paths[i]
            new_data_sructure[image_path] = detections_per_image
        
        self.new_data_structure = new_data_sructure


    def visualize(self , new_data = None):
        
        
        if new_data != None:
            self.new_data_structure = new_data
            
        data = self.new_data_structure
        data = list(zip(list(data.keys()) , list(data.values())))
        
        try:
            names =list((self.results[0][0].names).values())
        except Exception as e:
            print("Provide the dictionary mapping in self.names" )
            names = list(self.names.values())

        global class_color_dict
        class_color_dict = create_class_color_dict(names)
        
        def draw(data_):
            global class_color_dict
            image_p  , cords = data_
            image = Image.open(image_p)
            image = image.resize((320 , 320))
            image = np.array(image)

            for cord in cords:
                lab_ , _ , _ , points = cord
                boxesa = [int(float(i)) for i in points]
                
                image =  draw_single_box( image= image, boxes = boxesa,current_class= int(float(lab_)) , class_colors=class_color_dict , ready_cordinates= True , put_text=self.show_images_text )
            
            return image
        
        
        self.final_data = np.array(tuple(map(draw ,data )))
        
        names = list(self.new_data_structure.keys())
    
        if self.final_data.shape[0] < 3 or self.show_single:
            for i in range(self.final_data.shape[0]):
                cv2.imshow(os.path.basename(names[i]), self.final_data[i])
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            
            sub_plots(self.final_data)

    def save_detections(self):
        
        os.makedirs(self.output_dir , exist_ok=True)
                
        with open(os.path.join(self.output_dir,"dict.json") ,'w') as file:
            json.dump(self.results[0][0].names , file)
        
        if self.show_single:
            for image_path in self.new_data_structure:
                
                temp_dict = {image_path : self.new_data_structure[image_path]}
                image_name = os.path.basename(image_path)
                xml_file = os.path.join(self.output_dir , image_name) + '.xml'
                
                save_dict_to_xml(temp_dict , folder= xml_file)
            
        elif not self.show_single:
            save_dict_to_xml(self.new_data_structure , folder = self.output_dir)
        
        names = list(self.new_data_structure.keys())
       
        if self.final_data.shape[0] < 3 or self.show_single and self.save_images:
            for i in range(self.final_data.shape[0]):
                
                image_name = os.path.join( self.output_dir,  os.path.basename(names[i]))
                print("images saved : ", i +1 , self.output_dir)
            
                plt.imsave(image_name , self.final_data[i])
            
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            
        else:
            if self.save_images:
                sub_plots(self.final_data , save_fig=True , save_plot_to=self.output_dir , show_plot=False)

        
    def change_details(self):
        
        """
        Change details such as image directory, output directory, number of images, and confidence level.

        Switches:
            - 1: Change Image Directory
            - 2: Change Output Directory
            - 3: Change Number of Images
            - 4: Change Confidence Level
            - -5: Clear Console
            - p1: Show Single Plot
            - p2: Show Multiple Plots
            - SI: Save Images
            - SO: Do Not Save Images
            - 0: Go back

        Returns:
            None
        """
            
    
        
        while True:
            print("Choose an option to change:")
            print("1: Image Directory")
            print("2: Output Directory")
            print("3: Number of Images")
            print("4: Confidence Level")
            print('(p1, p2): sigle plot(p1) or multiple(p2)')
            print("(SI): save images , (SO): not save images")
            print("see: See current configurations")
            print("0: Go back")
            print("pt1 , pt0 : show images names when visualizing or not 0 == Off ")
            
            
    
            choice = input("Enter your choice: ")

            if choice == '0':
                break
            elif choice == '1':
                new_image_dir = get_folder_gui(self.image_dir_source)
                self.image_dir_source = new_image_dir
            elif choice == '2':
                new_output_dir = input("Enter the new output directory: ")
                self.output_dir = new_output_dir
                os.makedirs(self.output_dir, exist_ok=True)
            elif choice == '3':
                new_num_images = int(input("Enter the new number of images: "))
                self.num_images = new_num_images
            elif choice == '4':
                new_conf_level = float(input("Enter the new confidence level: "))
                self.min_conf = new_conf_level
            elif choice == '-5':
                clear_console()
            elif choice == 'p1':
                self.show_single = True
            elif choice == 'p2':
                self.show_single = False
                
            elif choice == 'SI':
                self.save_images = True
            elif choice == 'SO':
                self.save_images = False
            elif choice == 'see':
                yolo_model.print_configuration()
                
            elif choice == 'pt0':
                self.show_images_text = False
            elif choice == 'pt1':
                self.show_images_text = True    
                
            else:
                print("Invalid choice. Please choose a valid option.")
        
    def print_configuration(self):
        """
        Print the current configuration and attributes of the YOLOModel.

        This method dynamically retrieves and prints all mutable attributes.

        Returns:
            None
        """
        text = "##" * 10
        print(text)
        print("Current Configuration:")
        
        # Get all mutable attributes
        mutable_attributes = {attr: getattr(self, attr) for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")}
        
        for attribute, value in mutable_attributes.items():
            print(f"{attribute.capitalize().replace('_', ' ')}:", end=" ")

            # Check if the attribute is an image or dictionary
            if isinstance(value, (np.ndarray , list)):
                try:
                    value = np.array(value)
                    print(f"Shape: {value.shape}")
                except Exception as e:
                    print("Unkonw type")
            elif isinstance(value, dict):
                print(f"Num Elements: {len(value)}")
            else:
                print(value)

        print(text)



if __name__ == "__main__":
    yolo_model = YOLOModel(
        image_path="Images",
        min_conf=0.5,
        output_dir="YOLORESULTS",
        num_images=3
    )

    while True:
        print("Available choices:")
        print("b: Quit")
        print("s: Process Images")
        print("p: Predict")
        print("q: Save Detections")
        print("c: Change Details")
        print("v: Visualize")
        print("see: See current configurations")

        choice = input(": ")
        if choice == 'b':
            break
        elif choice == 's':
            yolo_model.process_images()
        elif choice == 'p':
            yolo_model.predict()
        elif choice == 'q':
            yolo_model.save_detections()
        elif choice == 'c':
            yolo_model.change_details()
        elif choice == 'v':
            yolo_model.visualize()
        elif choice == '-5':
            clear_console()
        elif choice == 'see':
            yolo_model.print_configuration()
        else:
            print("Invalid choice. Please choose a valid option.".upper())
            
            
























