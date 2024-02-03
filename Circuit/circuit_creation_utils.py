import numpy as np
import os , json
import glob
import random
from utils2 import join_break_xml , visualize_dict 
from utils import sub_plots

def get_cordinates(object_ , full_text , drawn_objects) :
    
    """
    Input :
    ------
        Tuple = (class_label , class_name , score , cordinates)
    
    
    Generates coordinates for drawing a circuit element based on the provided object data.

    Parameters:
    -----------
    object_ : tuple
        A tuple containing information about the circuit element, including class label, class name,
        score, and coordinates.
    full_text : str
        The current circuit information in a specific format.
    drawn_objects : list
        A list to store the drawn objects in the circuit diagram.
    line_list : list
        A list to store the line information of the circuit diagram.

    Returns:
    --------
    full_text : str
        The updated circuit information after adding the new element.
    """
    
    class_label , class_name , score , cordinates = object_
    
    new_cord = [ round(i * 2) for i in cordinates]
    
    
    xmin , ymin , xmax , ymax = new_cord
    vertical = False
    label = ''

    if "voltage" in class_name:
        label = 'v'
        vertical = True
    elif "resistor" in class_name:
        label = 'r'
    elif "capacitor" in class_name:
        label = 'c'
        
    elif 'junction' in class_name:
        label = 'w'
        
    elif "terminal" in class_name:
        label = 'g'
        
    elif "inductor" in class_name:
        label = 'l'
        
    elif "switch" in class_name:
        label = 's'
    
    if label != "v" or label == 'c':
        if xmax - xmin < ymax - ymin:
            vertical = True
    
    
    if 'junction' in class_name:
        if vertical:
            ymax = ymax-((ymax %ymin)/(3/4) )
        else:
            xmax = xmax  - ((xmax%xmin)/(3/4))
            
            
        x1 , y1 = xmax , ymin
        x2 , y2 = xmax , ymax
        x1 = round(x1/10) * 10 +np.random.randint(1 , 99)/ np.random.randint(39990 , 42220)
        x2 = round(x1/10) * 10 +np.random.randint(1 , 99)/ np.random.randint(39990 , 42220)
        y1 = round(y1/10) * 10 +np.random.randint(1 , 99)/ np.random.randint(39990 , 42220)
        y2 = round(y1/10) * 10  +np.random.randint(1 , 99)/ np.random.randint(39909 , 42220)
        
    else:
        if label == 'c':
            vertical = not vertical
            
            
        if vertical and not 'junction' in class_name: 
            x1,y1 = (xmax + xmin )/ 2 , ymin
            x2,y2  =  x1 ,ymax
            
            
        elif not vertical and not 'junction' in class_name:
            x1 , y1 = xmin , (ymax + ymin)/2
            x2,y2 = xmax , y1
            
        if not 'junction' in class_name:
            x1 = round(x1/10) * 10 +np.random.randint(7 , 99)/ np.random.randint(39990 , 42202)
            x2 = round(x2/10) * 10 +np.random.randint(7 , 99)/ np.random.randint(39990 , 42202)
            y1 = round(y1/10) * 10 + np.random.randint(7 , 99)/  np.random.randint(39990 , 42022)
            y2 = round(y2/10) * 10 + np.random.randint(7 , 99)/  np.random.randint(39990 , 42202)
            

    
    if not label  == None  and label != '' and full_text != None:
        # print(cordinates ,"===",x1/2,y1/2 ,"and ", x2/2,y2/2  , class_name , vertical) 
   
        drawn_objects.append((x1,y1 ,x2 ,y2 , label ,vertical))

        if label != 'w' and label != 'l' and label != 's' and label != 'v' and label != 'g':
            line = "{}\t{}\t{}\t{}\t{}\t0\t{}\n".format(label ,round(x1) , round(y1) , round(x2) , round(y2) , 100 )
            
        else:
            line = "{}\t{}\t{}\t{}\t{}\t0\n".format(label ,round(x1) , round(y1) , round(x2) , round(y2) )
        if label == 'c':
            line = line.strip("\n") +  "\t-4.999999999989599\t0.001\n"
            
        elif label == 'l':
            line = line.strip("\n") + "\t0.00001\t0\t0\n"
        elif label == 's':
            line = line.strip('\n') + "\t1\tfalse\n"
            
        elif label == 'v':
            line = line.strip('\n') + "\t0\t40\t50\t0\t0\t0.5\n"
        
        full_text = full_text + line
        

    return full_text


def use_get_cordinates(new_data_structure, dest_folder = "Schematics"):
    """
    Input is one large dictionary   
    Input ==  {
             File_name_1:[... , [label, object_name, score , "(x_min ,y_min , x_max , y_max)"] , ...  ] , 
             File_name_2:[.. , [label, "object_name", score, "(x_min ,y_min , x_max , y_max)"] , ...  ],
             }
    """
    os.makedirs(dest_folder , exist_ok=True)
    drawing_data = {}
    for p in new_data_structure:
        objects=new_data_structure[p]
        
 
        drawn = []
        full_text = "$\t1\t0.000005\t10.20027730826997\t50\t5\t50\t5e-11\n"
        
        for object_ in  objects:
            full_text = get_cordinates(object_ , full_text=full_text  , drawn_objects=drawn)
        
       
        name_ = os.path.splitext(os.path.basename(p))[0]
        path = os.path.join(dest_folder , name_)
        
        drawing_data[name_] = drawn , full_text 
           
        with open(path , 'w') as file:
            file.write(full_text)
            
    return drawing_data
  
def grab_new_data_structure(source = "YOLORESULTS" , num = 5):
    files = glob.glob(source + "/*.xml")

    if  len(files) < 2:
        files = files
        
    else:
        try:
            
            files = random.sample( files , num)
        except Exception as e:
            print("bringing all data")
            files = files

    final_dict = join_break_xml(files , task='j')

    final_data = visualize_dict(final_dict, show_names=True)
    print(final_data.shape)
    sub_plots(final_data[:1])
    
    return final_dict


if __name__ == "__main__":
    
    pass
