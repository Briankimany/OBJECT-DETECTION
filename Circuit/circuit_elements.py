

class Element():
    
    """
    A class representing an individual circuit element.

    Properties:
    -----------
    label : str
        The label or type of the circuit element.
    coordinates : tuple
        The coordinates of the circuit element.
    junctions : list
        List of junctions associated with the circuit element.

    Methods:
    --------
    get_label():
        Returns the label of the circuit element.

    get_coordinates():
        Returns the coordinates of the circuit element.

    get_junctions():
        Returns the junctions associated with the circuit element.
    """
    
    
    
    def __init__(self , data , count_dict = {} ,parent_circuit = None) -> None:
        
        """
        Initializes an Element object.

        Parameters:
        -----------
        data : tuple
            Information about the circuit element, including coordinates and label.
        count_dict : dict, optional
            Dictionary tracking the count of each object label.
        parent_circuit : Circuit, optional
            The parent circuit to which the element belongs.
        """
        
        
        
        self.x1 , self.y1 , self.x2 ,self.y2 ,self.label , _= data
        
        self.vertical = abs(round(self.x1) - round(self.x2)) < 5
        self.upper_junction = None
        self.lower_junction = None
        self.right_junction = None
        self.left_junction = None
        self.parent_circuit_connections = parent_circuit
        self.juntions_info = None
        
        
        
        if self.label in count_dict:
            count_dict[self.label] += 1
            name = self.label+"_"+str(count_dict[self.label])
            self.object_name= name
        else:
            count_dict[self.label] = 1
            
            name = self.label+"_"+str(count_dict[self.label])
            self.object_name= name
            
    
    def get_junctions_info(self):
        """
        
            self.juntions_info = {self.label: (self.upper_junction , self.lower_junction)}
            self.juntions_info = {self.label: (self.left_junction , self.right_junction)}
        """
        
        
        if self.vertical:
            self.juntions_info = {self.label: (self.upper_junction , self.lower_junction)}
        else:
            self.juntions_info = {self.label: (self.left_junction , self.right_junction)}
            
        return(self.juntions_info)
    

    def connect(self , source= None):
        if source != None:
            self.parent_circuit_connections = source
        if self.parent_circuit_connections != None:
            wire = False
            if self.vertical and self.upper_junction != None and self.lower_junction != None:
                str_wire1 = "w\t{}\t{}\t{}\t{}\t0\n".format(round(self.x1) , round(self.y1) , round(self.upper_junction[0]) , round(self.upper_junction[1]) )
                str_wire2 =  "w\t{}\t{}\t{}\t{}\t0\n".format(round(self.x1) , round(self.y2) , round(self.lower_junction[0]) , round(self.lower_junction[1]) )
                wire = True
                
            elif not self.vertical and self.right_junction != None and self.left_junction != None:          
                str_wire1 =   "w\t{}\t{}\t{}\t{}\t0\n".format(round(self.x2) , round(self.y2) , round(self.right_junction[0]) , round(self.right_junction[1]))
                str_wire2 =   "w\t{}\t{}\t{}\t{}\t0\n".format(round(self.x1) , round(self.y1) , round(self.left_junction[0]) , round(self.left_junction[1]))
                wire = True
                
            
            if wire:
                print(f"Here is the connection added {self.object_name}from {self.x1 , self.y1 , self.x2 , self.y2}\nconnection={str_wire1}: and 2{str_wire2}\n")
                if str_wire1 not in self.parent_circuit_connections and str_wire2 not in self.parent_circuit_connections:
                    self.parent_circuit_connections.extend([str_wire1 , str_wire2]) 
                else:
                    print("Connection Present" ,self.object_name ,str_wire1 , str_wire2 )
                    
            else:
                self.get_juntions_info() 
        else:
            print("Need parent Circuit in self.parent_circuit_connections")   
            
        return self.parent_circuit_connections     
