
from circuit_elements import Element

class Circuit():
    
    """
    Represents an electrical circuit composed of multiple elements.

    Attributes:
    - object_count_dict: Dictionary tracking the count of each object label.
    - circuit_elements: List of Element objects representing circuit elements.
    - juntions_dict: Dictionary mapping junction coordinates to Element objects.
    - sub_circuit_dict: Dictionary mapping junction coordinates to sub-circuit elements.
    - vertical_juntion_pairs_dict: Dictionary mapping average x-values to pairs of vertical junctions.
    - horizontal_juntion_dict: Dictionary mapping y-values to lists of horizontal junctions.
    - circuit_name: Name assigned to the circuit.

    Methods:
    - get_juntions(): Identifies junctions within the circuit layout.
    - split_circuit(): Divides the circuit into sub-circuits based on x-axis alignment.
    - join_elements(): Joins circuit elements based on assigned junctions.
    """
    
    
    
    def __init__(self, objects_list , circuit_name = None ) -> None:
        
        
        """
        Initializes a Circuit object.

        Parameters:
        -----------
        objects_list : list
            List of objects representing circuit elements.
        circuit_name : str, optional
            The name assigned to the circuit.
        """
        
        
        
        self.object_count_dict= {}
        self.circuit_elements = [Element(i , count_dict=self.object_count_dict) for i in objects_list]
        self.juntions_dict= {}
        self.sub_circuit_dict = {}
        self.vertical_juntion_pairs_dict = {}
        self.horizontal_juntion_dict = {}
        self.cirtcuit_name = circuit_name
        
        
    def get_juntions(self):
        
        y_corner_dict = {}
        
        count = 0
        prev_ = None
        for object_ in self.circuit_elements:
            if object_.label == 'w':
                count += 1

                self.juntions_dict[object_.x2] = object_

                  
                y_corner_dict[object_.y2] = object_

        first = True   
        for juntion in self.juntions_dict:
            current_juntion = self.juntions_dict[juntion]
            
            if first:
                prev_juntion_value = current_juntion.x2 
            
            else:
                
                # print(f"Prev juntion {prev_juntion_value.x2} current _juntion {current_juntion.x2} modeulus { max(current_juntion.x2 , prev_juntion_value.x2) % min(current_juntion.x2 , prev_juntion_value.x2)}" )
                if  max(current_juntion.x2 , prev_juntion_value.x2) % min(current_juntion.x2 , prev_juntion_value.x2) < 20:
                    average_value = round( (current_juntion.x2 + prev_juntion_value.x2) / 2)
                    
                    upper_corner , lower_corner =     min(current_juntion.y2 , prev_juntion_value.y2)   , max(current_juntion.y2 , prev_juntion_value.y2)
                    
                    self.vertical_juntion_pairs_dict[average_value] = [y_corner_dict[upper_corner] ,y_corner_dict[lower_corner] ] 
                    
                else:
                   pass
                    # print("range is too large " , prev_juntion_value.x2 , current_juntion.x2)
                    
            first = False
            prev_juntion_value = current_juntion    
            
            
        for juntion in self.juntions_dict:
            current_juntion = self.juntions_dict[juntion]
            
            if current_juntion.y1 not in self.horizontal_juntion_dict:
                self.horizontal_juntion_dict[current_juntion.y1] = [current_juntion]
                
            else:
                self.horizontal_juntion_dict[current_juntion.y1].append(current_juntion)
                
                   
    def split_circuit(self):
        """
        Divides the circuit into sub-circuits based on x-axis alignment.

        Algorithm:
        -----------
        - Identify vertical junction pairs.
        - Iterate through junction pairs:
            - Determine average x-value between junction pairs.
            - Find objects within the range of the current junction pair.
            - Assign upper and lower junctions to vertical objects.
            - Assign left and right junctions to horizontal objects.
            - Add objects to the temporary circuit elements list.
            - Update the sub-circuit dictionary with the elements.
        """
        
        
        temp_circuit_elemnts_list = []
        
        def compare_juntion(self, temp_circuit_elemnts_list, junction_value, prev_junction):
            average_value = round((junction_value.x2 + prev_junction.x2) / 2)
            top_corner, lower_corner = self.vertical_juntion_pairs_dict[average_value]
            self.junctions_list = sorted(list(self.vertical_juntion_pairs_dict.keys()))
            
            next_jun_index = (self.junctions_list.index(average_value) +1)
            if next_jun_index < len(self.junctions_list):
                next_juntion_key =  self.junctions_list[ next_jun_index]
                next_top , next_lower = self.vertical_juntion_pairs_dict[next_juntion_key]
                next_junction = next_top
            else:
                print("we have reached the end")
                next_junction = None
                next_juntion_key =  self.junctions_list[(next_jun_index-2)]
                next_top , next_lower = self.vertical_juntion_pairs_dict[next_juntion_key]
            
            for object_ in self.circuit_elements:
                
                # print("evaluating object for this average" , average_value, object_.object_name )
                if object_.label != 'w' and object_ not in temp_circuit_elemnts_list:
                    
                    if next_junction == None:
                        in_range = True
                        
                        
                    elif object_.x1 > junction_value.x1 and object_.x2 < next_junction.x1:
                        in_range = True
                        
                    elif abs (object_.x1 - junction_value.x1) < 35 and abs(object_.x2 - next_junction.x1) < 35:
                        
                        in_range = True
                        
                    elif abs (object_.x1 - junction_value.x1) < 35 and object_.x2 < next_junction.x1:
                        in_range = True
                        
                    elif abs(object_.x2 - next_junction.x1) < 35 and object_.x1 > junction_value.x1 :
                        in_range = True
                        
                    else:
                        in_range = False
       

                    if next_junction != None:
                        vas =  next_junction.x1
                    else:
                        vas = next_junction
                    # print("object name",  object_.object_name , f"x cordinates = ({object_.x1 , object_.x2})::in_range={in_range}:limits= {junction_value.x1,vas}" )
                    # print("Object under evaluation " , object_.object_name , object_.vertical , "limits" ,top_corner.x1 ,vas ,in_range)
            
                    # object_distance_from_average_x_value = abs(object_.x1 - average_value)
                    # print(object_.object_name , object_distance_from_average_x_value)
                    
                    # Check if the object is within the acceptable range from the average x value
                   
                    if  in_range:
                        
                        if object_.vertical:
                            object_distance_from_average_x_value = abs(object_.x1 - top_corner.x1) 
                            # For vertical objects, assign upper and lower junctions
                            if next_junction!= None:
                                if object_distance_from_average_x_value < 30:
                                    object_.upper_junction = (top_corner.x1, top_corner.y1)
                                    object_.lower_junction = (lower_corner.x2, lower_corner.y2)
                                else:
                                    object_.upper_junction = (next_top.x1, next_top.y1)
                                    object_.lower_junction = (next_lower.x2, next_lower.y2)

                        else:
                            
                            object_distance_from_average_y_value = abs (object_.y1 - top_corner.y1)
                            top = object_distance_from_average_y_value < 50
                            
                            if top:
                                print("at teh top" , object_.object_name  , top_corner.x1, top_corner.y1)
                                object_.left_junction = (top_corner.x1, top_corner.y1)
                                object_.right_junction = (next_top.x1 , next_top.y1)
                                
                            else:
                                print("not top" , object_.object_name)
                                object_.left_junction = (lower_corner.x1, lower_corner.y1)
                                object_.right_junction = (next_lower.x1 , next_lower.y1)
                        
                        # Add the object to the temporary list and sub-circuit dictionary
                        temp_circuit_elemnts_list.append(object_)
                        self.sub_circuit_dict[average_value].append(object_)
                        
                
                elif object_ in temp_circuit_elemnts_list:
                    pass
                    # print("This has been added already ", object_.object_name)
                    
                else:
                    pass
                    # print("UNUSED",object_.object_name )
                    
            print("\n\n")
            return temp_circuit_elemnts_list
        
        for junction in self.vertical_juntion_pairs_dict:
            prev_juntion , junction_value  = self.vertical_juntion_pairs_dict[junction]
            self.sub_circuit_dict[junction] = []
            # print("Here is the average subcircuit being compared" ,"x_values is " , average_value, "upper_corner is ", upper.y1 , "lower_corner",loer.y1)
            temp_circuit_elemnts_list= compare_juntion(self ,temp_circuit_elemnts_list, junction_value , prev_juntion ) 
            
        print(temp_circuit_elemnts_list)
        self.kim = temp_circuit_elemnts_list
            


if __name__ == "__main__":
    
    pass
