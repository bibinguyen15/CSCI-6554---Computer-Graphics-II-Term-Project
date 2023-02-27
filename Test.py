import OpenGL
import OpenGL.GL
import OpenGL.GLUT



def readFile(fileName):
    with open(fileName, 'r') as f: 
        #split each line into a data index
        data = f.readlines()
        
        #number  of vertices and number of polygons
        nVer, nPol = int(data[0].split()[1]), int(data[0].split()[2])
        
        vertices, poly = [], []
        
        #processing the vertices
        vertices =[]
        for i in range(nVer):
            print(i)
            
        
        #processing the polygons
        for i in range(nPol):
            print(i)
        
        
        
       
    
    
    
readFile("house.d.txt")


