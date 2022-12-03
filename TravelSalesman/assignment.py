import operator
import csv
import math
import queue as Q
import copy
from numpy import empty
import time

#Class for craeting nodes which are used in a_star search 
class Node:

    def __init__(self,parent,position):
        self.parent=parent
        self.position=position
        self.g=0
        self.h=0
        self.f=0

#Class for creating nodes which are used in UCS
class UCS_node:

    def __init__(self, current_name):
        self.visited = []
        self.current = current_name
        self.cost = 0
        self.completed = False
        self.add_visited(current_name)

    def add_visited(self, node_name):
        self.visited.append(node_name)

    def current_node(self, node_name, cost):
        self.current = node_name
        self.add_visited(node_name)
        self.add_cost(cost)
    
    def add_cost(self, new_cost):
        self.cost += new_cost
    
    def get_name(self):
        return self.current

#a_star search algorithm for shortest path graph
def A_star(graph,start,end):

    start_node = Node(None,start)
    start_node.g=0
    start_node.h=abs(start[0]-end[0]) + abs(start[1]-end[1])
    start_node.f=start_node.g + start_node.h

    open=[]
    closed=[]

    open.append(start_node)
    while len(open) > 0:
        open.sort(key=lambda n: n.f)
        current_node=open.pop(0)
        closed.append(current_node)
        if current_node.position == end:
            path=[]
            while current_node.parent != None:
                path.append(current_node.position)
                current_node=current_node.parent

            return start,end,len(path)

        x,y = current_node.position

        neighbor_nodes = [(x-1,y),(x,y+1),(x,y-1),(x+1,y)]
        children=[]
        for neighbor_node in neighbor_nodes:
            neighbor_nodeValue=graph[neighbor_node[0]][neighbor_node[1]]
            if neighbor_nodeValue == "*":
                continue
            child_node = Node(current_node,neighbor_node)

            child_node.g=abs(child_node.position[0]-start[0]) + abs(child_node.position[1]-start[1])
            child_node.h=abs(child_node.position[0]-end[0]) + abs(child_node.position[1]-end[1])
            child_node.f = child_node.g + child_node.h
            
            children.append(child_node)

        for child in children:

            for child_closed in closed:
                if child == child_closed:
                    continue
            
            
            #print(child.g)
            for child_open in open:
                if child == child_open and child.g > child_open.g:
                    continue
                    
            open.append(child)

# BFS 
def bfs(graph):

    visited=[]
    queue = []
    path=[]
    total_cost=0
    queue.append("a")

    while queue:
        n=queue.pop(0)
        path.append(n)
        #print(n,end=" ")

        for next in graph[n]:
            if next not in visited:
                #print(total_cost)
                total_cost+=graph[n][next]
                visited.append(next)
                queue.append(next)
    
    return path,total_cost

# UCS
def ucs(graph):
    node = UCS_node("a") 
    queue = []
    queue.append(node)
    path=[]
    counter = 0
    while True:
        
        queue = sorted(queue, key=operator.attrgetter('cost')) 
        # print(counter,"::::",queue[0].current)

        node= queue.pop(0)
        # print("node name : ", node.current, "node cost : ", node.cost)

        if "a" in node.visited and "b" in node.visited and "c" in node.visited and "d" in node.visited and "a" in node.visited and node.completed == True:
            # print("minimum cost of the way is : ", node.cost)
            
            for name in node.visited:
                path.append(name)
                #print(name)
            return path,node.cost

        counter += 1

        if node.completed == False:

            for node_name in graph[node.get_name()]:
                
                # print("node name : ",node_name)
                
                if node_name not in node.visited:  
                    
                    process_node = copy.deepcopy(node)
                    cost = graph.get(node.current, {}).get(node_name)
                    process_node.current_node(node_name,cost)
                    queue.append(process_node)
                    # print("process node cost: ", process_node.cost )
                    # print("\nqueue len", len(queue))

                elif len(node.visited) >= 3:
                    process_node = copy.deepcopy(node)
                    cost = graph.get(node.current, {}).get(node_name)
                    process_node.current_node(node_name,cost)
                    if(node_name == 'a'):
                        process_node.completed = True
                        # print("completed")
                    queue.append(process_node)
                    # print("process node cost: ", process_node.cost )
                    # print("\nqueue len", len(queue))

                else:
                    continue

# Converts coordinates to letters for better understanding
def convertCoordinateToLetter(x,arr):

    if x == arr[0]:
        return "a"
    elif x == arr[1]:
        return "b"
    elif x == arr[2]:
        return "c"
    elif x == arr[3]:
        return "d"

# Reads the map file and creates the shortest path graph
def read_map_file():
    with open("map.txt") as f:
        line = f.readline()
        num_cols = len(line.strip())
        row=0
        f.seek(0)
        for line in f:
            row+=1
        f.seek(0)
        arr=[]
        for line in f:
            arr.append(line.strip())

    coordinates=[[]for i in range(4)]
    for i,x in enumerate(arr):
        if "A" in x:
            A=(i,x.index("A"))
            coordinates[0]=(i,x.index("A"))
        if "B" in x:
            B=(i,x.index("B"))
            coordinates[1]=(i,x.index("B"))
        if "C" in x:
            C=(i,x.index("C"))
            coordinates[2]=(i,x.index("C"))
        if "D" in x:
            D=(i,x.index("D"))
            coordinates[3]=(i,x.index("D"))
    
    #print(coordinates)

    adj=[]
    c=4
    i=0

    while i < len(coordinates):
        j=i+1
        while j < c:
            if coordinates[i] == B and coordinates[j] == D:
                start,end,weight=A_star(arr,coordinates[j],coordinates[i])
                s=convertCoordinateToLetter(end,coordinates)
                e=convertCoordinateToLetter(start,coordinates)
                adj.append((s,e,weight))
            else:    
                start,end,weight=A_star(arr,coordinates[i],coordinates[j])
                s=convertCoordinateToLetter(start,coordinates)
                e=convertCoordinateToLetter(end,coordinates)
                adj.append((s,e,weight))
            j+=1
        i+=1
    return adj,coordinates

# Creates a secondary graph using first graph for easier solutions in UCS and BFS
def create_graph(adj,coordinates):

    new_adj=[]

    for i in adj:
        new_adj.append(i)
        new_adj.append((i[1],i[0],i[2]))

    graph={}
    letters=[]

    for i in coordinates:
        letters.append(convertCoordinateToLetter(i,coordinates))

    for j in letters:
        graph[j]={}
        for i in new_adj:
            if i[1]=="a":
                continue
            if i[0]==j:
                graph[j][i[1]]=i[2]
    for j in letters:
        if j=="a":
            continue
        for i in new_adj:
            if i[1]=="a" and i[0]==j:                
                graph[j].update({i[1]:i[2]})

    return graph

# main
if __name__=="__main__":

    print("\n---Welcome to the Travelling Salesman Problem---\n")
    print("1. Construct the shortest path graph\n")
    print("2. TSP Solution with BSF and UCS\n")
    print("3. Exit\n")

    choice=int(input("Enter your choice "))

    while choice ==1 or choice == 2:

        if choice == 1:
            adj,coordinates=read_map_file()
            print("----------------")
            print("\nShortest Path graph is constructed!!!\n")
            print("----------------")
            print("Shortest Path Graph\n")
            print("\n".join("{},{},{}".format(*i) for i in adj)+"\n")
            print("----------------")
        
        elif choice == 2:
            graph=create_graph(adj,coordinates)
            start_time = time.time()
            ucs_path,ucs_cost=ucs(graph)
            ucs_process_time = time.time() - start_time#get process time
    
            #print(ucs_path,ucs_cost)
            #print(ucs_process_time)

            start_time = time.time()
            bfs_path,bfs_cost=bfs(graph)
            bfs_process_time = time.time() - start_time#get process time

    #print(bfs_process_time)
    
            print("----------------")
            print("\nAlgorithm Used: BFS\n")
            print("\n".join(bfs_path)+"\n")
            print("Total Tour Cost:{}\n".format(bfs_cost))
            print("----------------")
            print("Algorithm Used: UCS\n")
            print("\n".join(ucs_path)+"\n")
            print("Total Tour Cost: {}".format(ucs_cost)+"\n")
            print("----------------")
            print("Statistics:\n")
            print("Nodes            Time                    Cost\n")
            print("BFS "+"-".join(bfs_path)+"   "+"  {} (Nearly)            {}".format(bfs_process_time,bfs_cost))
            print("UCS "+"-".join(ucs_path)+"   "+"  {}   {}".format(ucs_process_time,ucs_cost))
            print("----------------\n")

        print("1. Construct the shortest path graph\n")
        print("2. TSP Solution with BSF and UCS\n")
        print("3. Exit\n")
        choice=int(input("Enter your choice "))

    print("BYEEEE!!!")
    

    #print(graph)

   
           

