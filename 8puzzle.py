
import re
import sys
import copy as cp

hueristics_list=[]
generated=[]

class eight_puzzle():
    #Init function will compile a regular exp where \d is a digit followed by a \s that is a whitespace & input verification
    def __init__(self, str):
        regex = re.compile("(\d)\s(\d)\s(\d)\s(\d)\s(\d)\s(\d)\s(\d)\s(\d)\s(\d)") #
        result = regex.match(str)
        if result is not None:
            x = result.groups()
            self.state = [[int(x[0]), int(x[1]), int(x[2])],
                          [int(x[3]), int(x[4]), int(x[5])],
                          [int(x[6]), int(x[7]), int(x[8])]]
        else:
            print("Input error!")

    #To return a string rep of the input matrix
    def __str__(self):
        x = ''
        for i in range (0,3):
            for j in range(0,3):
                x += str(self.state[i][j]) + ' '
        return x

    #Doing equality checks with eq and ne 
    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False
        
    def __ne__(self, other):
        return not self.__eq__(other)
        
    #For performing operations on a set
    def __hash__(self):
        uid = 0
        mult = 1
        for i in range(0,3):
            for j in range(0,3):
                uid += self.state[i][j] * mult
                mult *= 9
        return uid

    #Function for implementing misplaced tiles              
    def misplaced_tiles(self, goal):
        sum = 0
        for i in range(0, 3):
            for j in range(0, 3):
                if (self.state[i][j] != goal.state[i][j]):
                    sum += 1
        return sum

    #Function for implementing Manhattan Distance     
    def manhattan(self, goal):
        sum = 0
        for i in range(0, 3):
            for j in range(0, 3):
                tile = self.state[i][j]
                for m in range(0, 3):
                    for n in range(0, 3):
                        if tile == goal.state[m][n]:
                            sum += abs(i-m) + abs(j+n)
        return sum

    #Checking feasible next moves from a particular state
    def achievable_states(self):
        list = []
        idx = self.get_tile_zero()
        x = idx[0]
        y = idx[1]
        if x > 0:
            r = cp.deepcopy(self)
            r.state[y][x] = r.state[y][x-1]
            r.state[y][x-1] = 0
            list.append((r,'r'))
        if x < 2:
            l = cp.deepcopy(self)
            l.state[y][x] = l.state[y][x+1]
            l.state[y][x+1] = 0
            list.append((l,'l'))
        if y > 0:
            d = cp.deepcopy(self)
            d.state[y][x] = d.state[y-1][x]
            d.state[y-1][x] = 0
            list.append((d,'d'))
        if y < 2:
            u = cp.deepcopy(self)
            u.state[y][x] = u.state[y+1][x]
            u.state[y+1][x] = 0
            list.append((u,'u'))
        return list
        
    def get_tile_zero(self):
        for i in range(0, 3):
            for j in range(0, 3):
                if self.state[i][j] == 0:
                    x = j
                    y = i
        return (x,y)

    #A* algorithm -- Storing nodes in a fringe, closed list, expanding nodes from the neighbour
    def aStarSearch(self, goal, heuristic, output):
        closed_list = set()      
        fringe_list = set([self])
        prev = {}
        sum=0
        gOfn = {self : 0}
        fOfn = {self : gOfn[self] + heuristic(self,goal)}
        
        while (len(fringe_list) != 0):
            current = None
            for node in fringe_list:
                if current is None or fOfn[node] < fOfn[current]:
                    current = node
            if current == goal:
                return output(self, prev, current, heuristic)
                
            fringe_list.remove(current)
            closed_list.add(current)
            sum=0
            for n in current.achievable_states():
                sum+=1
                neighbour = n[0]
                if neighbour in closed_list:
                    continue
                temp_gOfn = gOfn[current] + 1
                
                if neighbour not in fringe_list or temp_gOfn < gOfn[neighbour]:
                    prev[neighbour] = (current, n[1])
                    gOfn[neighbour] = temp_gOfn
                    h=heuristic(neighbour,goal)
                    fOfn[neighbour] = gOfn[neighbour] + h
                    if neighbour not in fringe_list:
                        fringe_list.add(neighbour)
            generated.append(sum)
        return "empty"

    #State transition using selected heuristic
    def transition(self, prev, current_node, heuristic):
        goal = current_node
        return self.action_transition(prev, current_node, goal, heuristic)
             
    #Checking for a goal
    def action_transition(self, prev, current_node, goal, heuristic):
        delimiter = "\n"
        if current_node == goal:
            delimiter = ""
        if current_node in prev:
            p = self.action_transition(prev, prev[current_node][0], goal, heuristic)
            p += str(current_node) + delimiter
            hueristics_list.append(heuristic(current_node, goal))
            return p
        else:
            return str(current_node) + delimiter


# Main Function -- take inputs & call functions
def main():
	start = []
	print ("\nINITIAL CONFIGURATION")
	print ("Enter values for \n\n 1X1|1X2|1X3 \n ----------- \n 2X1|2X2|2X3 \n ----------- \n 3X1|3X2|3X3 \n\n Please enter 0 as the blank tile ")
	user_input = input("Enter value for 1X1: ")
	start.append(user_input)
	user_input = input("Enter value for 1X2: ")
	start.append(user_input)
	user_input = input("Enter value for 1X3: ")
	start.append(user_input)
	user_input = input("Enter value for 2X1: ")
	start.append(user_input)
	user_input = input("Enter value for 2X2: ")
	start.append(user_input)
	user_input = input("Enter value for 2X3: ")
	start.append(user_input)
	user_input = input("Enter value for 3X1: ")
	start.append(user_input)
	user_input = input("Enter value for 3X2: ")
	start.append(user_input)
	user_input = input("Enter value for 3X3: ")
	start.append(user_input)

	initial_input = (' '.join(map(str, start)))
	
	end = []
	print ("\nGOAL CONFIGURATION")
	print ("Enter values for \n\n 1X1|1X2|1X3 \n ----------- \n 2X1|2X2|2X3 \n ----------- \n 3X1|3X2|3X3 \n\n Please enter 0 as the blank tile ")
	user_input = input("Enter value for 1x1: ")
	end.append(user_input)
	user_input = input("Enter value for 1x2: ")
	end.append(user_input)
	user_input = input("Enter value for 1x3: ")
	end.append(user_input)
	user_input = input("Enter value for 2x1: ")
	end.append(user_input)
	user_input = input("Enter value for 2x2: ")
	end.append(user_input)
	user_input = input("Enter value for 2x3: ")
	end.append(user_input)
	user_input = input("Enter value for 3x1: ")
	end.append(user_input)
	user_input = input("Enter value for 3x2: ")
	end.append(user_input)
	user_input = input("Enter value for 3x3: ")
	end.append(user_input)

	goal_input = ' '.join(map(str, end))

        print("Choose your hueristic: \n")
    	print ("1.Misplaced Tiles")
    	print ("2.Manhattan distance \n")
    
    	h = input("Enter your choice: ")
    	if h == 1:
            heuristic = eight_puzzle.misplaced_tiles
    	elif h == 2:
        	heuristic = eight_puzzle.manhattan
    
    	output = eight_puzzle.transition
    
    	initial = eight_puzzle(initial_input)
    	goal = eight_puzzle(goal_input)
    
    	result = initial.aStarSearch(goal, heuristic, output)
    	count=0
    	g=1
    	j=0
    	res=''
    	sum=0
    	for i in result:
		if i==' ':
			count+=1
		if(count==3):
			res+='\n'
			count=0
		elif i=='\n':
			res+="\n"
			print
			g+=1
			j+=1
		else:
			res=res+i
    	for i in generated:
		sum+=i		
   	print (res)
    	print ("Nodes Generated = "),sum
    	print ("Nodes Expanded = "),j
    
if __name__ == '__main__':
    main()
