import random
import itertools
import collections
import time
import operator
from tkinter import *






class Node:
    """
    A class representing an Solver node
    - 'puzzle' is a Puzzle instance
    - 'parent' is the preceding node generated by the solver
    - 'action' is the action taken to produce puzzle
    _ 'g' is cost from start to current node
    - 'h is heuristic based estimated cost for current Node to end Node
    - 'f' is total cost of present Node e.g. : f = g + h
    """

    def __init__(self, puzzle, heur, parent=None, action=None):
        self.puzzle = puzzle
        self.parent = parent
        self.action = action
        self.heur = heur # heur de type string = 'H1' or 'H2'
        
        if(self.heur == 'H1'):
            self.h = self.puzzle.mal_placé()
        elif(self.heur == 'H2'):
            self.h = self.puzzle.distance_heuristic()
        if (self.parent != None):
            self.g = parent.g + 1    #profondeur de l'arbre
        else:
            self.g = 0
        self.f = self.g + self.h
        


    "Return a hashable representation of self"
    @property
    def state(self):
        return str(self)

    "Reconstruct a path from to the root 'parent'"
    @property 
    def path(self):
        node, p = self, []
        while node:
            p.append(node)
            node = node.parent
        yield from reversed(p)

    " Wrapper to check if 'puzzle' is solved "
    @property
    def solved(self):
        return self.puzzle.solved

    " Wrapper for 'actions' accessible at current state "
    @property
    def actions(self):
        return self.puzzle.actions

    def __str__(self):
        return str(self.puzzle)

   




class Solver:

    def __init__(self, start ,fenetre):
        self.start = start
        self.fenetre = fenetre


    """
    Perform breadth first search and return a path
        to the solution, if it exists
    """
    def solve(self,heur):
        
        if(heur == 'H1'):
            print("Recherche de solution avec heuristic 1")
        elif(heur == 'H2'):
            print("Recherche de solution avec heuristic 2")
        print(self.start.board)
        global j
        queue = collections.deque([Node(self.start,heur)])
        closed = set() #ensemble contenant les noeuds developpés: "closed"
        closed.add(queue[0].state)
        
        while queue:
            opened= []
            node = queue.popleft() # on developpe la téte de la file ayant heuristic minimal
            if node.solved:
            	z= list(node.path)
            	self.affRes(z)
            	print("solution trouvée en", len(z) , " coups")
            	break
            for move, action in node.actions:
                child = Node(move(),heur, node, action)
                if child.state not in closed:
                    opened.append(child) # create childs list: "opened"
            opened.sort(key = operator.attrgetter('f')) # file triée selon l'heuristique
            for ch in opened:
                queue.append(ch)
                closed.add(ch.state)
                    
            

        
    def affRes(self , p , i=1):
    	node = p[0]
    	p=p[1:]
    	x=node.puzzle.convL()
    	print("coup",i," : ",x)
    	node.puzzle.afficherImg(x)
    	if p:
            self.fenetre.after(1500, self.affRes, p, i+1)
    	else :
        	print("fin")


class Puzzle:

    """
    A class representing an '8-puzzle'.
    - 'board' should be a square list of lists with integer entries 0...width^2 - 1
       e.g. [[1,2,3],[4,0,6],[7,5,8]]
    """
    def __init__(self, board , root , listPhotos):
        self.width = len(board[0]) #=3
        self.board = board #matrice contenant les nbres 
        self.can = root
        self.listPhotos = listPhotos


    """
        The puzzle is solved if the flattened board's numbers are in
        increasing order from left to right and the '0' tile is in the
        last position on the board
    """
    @property
    def solved(self):

        tab = []
        solved = True
        for i in range (self.width):
	        tab.extend(self.board[i])

        for j in range (len(tab)-2):
        	if (tab[j]!=(tab[j+1]-1)):
        		solved = False
        if tab[-1] != 0 :
        	solved = False
        return solved


    "h1 = number of badly placed pieces"    
    def mal_placé(self):
        etat_final=[[1,2,3],[4,5,6],[7,8,0]]
        n=0
        for i in range(3):
            for j in range(3):
                if (self.board[i][j]!=etat_final[i][j]):
                    n = n+1
        return n

    "correct place of value x"
    def placeCorrect(self,x):
        but = [[1,2,3],[4,5,6],[7,8,0]]
        for i in range(3):
            for j in range(3):
                if(but[i][j] == x):
                    result = [i,j]
                    return(result)

    "h2 = sum distances of each piece to its final position"
    def distance_heuristic(self):
        n = 0
        for i in range(3):
            for j in range(3):
                if (self.board[i][j] != 0):
                    ind = self.placeCorrect(self.board[i][j])
                    n = n + abs(ind[0] - i) + abs(ind[1] - j)
        return n


    """
    Return a list of 'move', 'action' pairs. 'move' can be called
    to return a new puzzle that results in sliding the '0' tile in
    the direction of 'action'.
    """
    @property 
    def actions(self):
        def create_move(at, to):
            return lambda: self.move(at, to)

        moves = []
        for i, j in itertools.product(range(self.width),
                                      range(self.width)):
            direcs = {'R':(i, j-1),
                      'L':(i, j+1),
                      'D':(i-1, j),
                      'U':(i+1, j)}

            for action, (r, c) in direcs.items():
                if r >= 0 and c >= 0 and r < self.width and c < self.width and self.board[r][c] == 0:
                    move = create_move((i,j), (r,c)), action
                    moves.append(move) #liste des paires(nouvelle matrice , operateur)
        return moves

    """
    Return a new puzzle that has been shuffled with 500 random moves
    """
    def shuffle(self):
        puzzle = self
        for k in range(1000):
            puzzle = random.choice(puzzle.actions)[0]()
        x=puzzle.convL()
        print(x)
        self.afficherImg(x)
        self = puzzle
        puzzle.board = self.board
        return puzzle

    """
    Return a new puzzle with the same board as 'self'
    """
    def copy(self):
        board = []
        for row in self.board:
            board.append([x for x in row])
        return Puzzle(board,self.can,self.listPhotos)

    """
    Return a new puzzle where 'at' and 'to' tiles have been swapped.
    Ps: all moves should be 'actions' that have been executed
    """
    def move(self, at, to):
        copy = self.copy()
        i, j = at
        r, c = to
        copy.board[i][j], copy.board[r][c] = copy.board[r][c], copy.board[i][j]
        return copy

    "display images on canvas"
    def afficherImg (self,liste1):
        for k in range(len(liste1)) :
            eff =self.can.create_image((30+ 150*(k % self.width)), 30+(150*( k // self.width)), anchor=NW, image=self.listPhotos[0])
            aff =self.can.create_image((30+ 150*(k % self.width)), 30+(150*( k // self.width)), anchor=NW ,image = self.listPhotos[liste1[k]])


    "display the board in the console"
    def pprint(self):
        for row in self.board:
            print(row)
        print()
    
    "return the board as a table"
    def convL(self):
    	L=[]
    	for row in self.board:
    		L.extend(row)
    	return L 

    def __str__(self):
        return ''.join(map(str, self))

    def __iter__(self):
        for row in self.board:
            yield from row
