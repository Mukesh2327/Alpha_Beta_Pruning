#importing time module to measure the time of evaluation 
import time 
class Game:
    def __init__(self):
        self.initialize_game()
    
    #initialization of game parameters(initial empty board creation)
    def initialize_game(self):
        self.current_state=[['.','.','.'],['.','.','.'],['.','.','.']]
        self.player_turn='X'
    
    # for drawing the board
    def draw_board(self):
        for i in range(0,3):
            for j in range(0,3):
                print('{}|'.format(self.current_state[i][j]),end=' ')
            print()
        print()
    
    # for checking whether a move is legal or not 
    def is_legal_move(self,x,y):
        if x<0 or x>2 or y<0 or y>2:
            return False
        elif self.current_state[x][y]!='.':
            return False 
        else :
            return True 
    
    #check if the game is finished and return the winner
    def is_game_finished(self):
        #vertical win 
        for j in range(0,3):
            if self.current_state[0][j]!='.' and self.current_state[0][j]==self.current_state[1][j] and self.current_state[1][j]==self.current_state[2][j]:
                return self.current_state[0][j]
        
        #horizontal win 
        for i in range(0,3):
            if self.current_state[i]==['X','X','X']:
                return 'X'
            elif self.current_state[i]==['O','O','O']:
                return 'O'
        
        #main diagonal 
        if self.current_state[0][0]!='.' and self.current_state[0][0]==self.current_state[1][1] and self.current_state[1][1]==self.current_state[2][2]:
            return self.current_state[0][0]
        
        #second diagonal 
        if self.current_state[0][2]!='.' and self.current_state[0][2]==self.current_state[1][1] and self.current_state[1][1]==self.current_state[2][0]:
            return self.current_state[0][2]
        
        #board is full 
        for i in range(0,3):
            for j in range(0,3):
                if self.current_state[i][j]=='.':
                    return None 
        
        #if it's a tie 
        return '.'


    # Player 'O' is max, in this case AI
    def max_alpha_beta(self,alpha,beta):
        # Possible values for maxv are:
        # -1 - loss
        # 0  - a tie
        # 1  - win

        # We're initially setting it to -2 as worse than the worst case:
        maxv=-2

        #these are the position where AI automatically does the move in order to maintain optimality
        x=None 
        y=None

        result=self.is_game_finished()

        # If the game came to an end, the function needs to return
        # the evaluation function of the end. That can be:
        # -1 - loss
        # 0  - a tie
        # 1  - win 
        
        if result=='X':
            return (-1,0,0)
        elif result=='O':
            return (1,0,0)
        elif result=='.':
            return (0,0,0)

        
        for i in range(0,3):
            for j in range(0,3):
                if self.current_state[i][j]=='.':
                    
                    # On the empty field player 'O' makes a move and calls Min
                    # That's one branch of the game tree.

                    self.current_state[i][j]='O'

                    (m,min_i,min_j)=self.min_alpha_beta(alpha,beta)

                    # Fixing the maxv value if needed(for making the overall logic v<-Max(v,Min_Val(alpha,beta)))
                    if m>maxv:
                        maxv=m 
                        x=i
                        y=j 

                    # Setting back the field to empty
                    self.current_state[i][j]='.'

                    #pruning step
                    if m>=beta:
                        return (maxv,x,y)

                    #setting the alpha value
                    if maxv>alpha:
                        alpha=maxv 
        return(maxv,x,y )

    # Player 'X' is min, in this case human
    def min_alpha_beta(self,alpha,beta):
        # Possible values for minv are:
        # -1 - win
        # 0  - a tie
        # 1  - loss

        # We're initially setting it to 2 as worse than the worst case:
        minv=2

        #these variables are just the recommended position where human should place his move in order to have optimal or zero-sum game
        x=None 
        y=None

        result=self.is_game_finished()

        # If the game came to an end, the function needs to return
        # the evaluation function of the end. That can be:
        # -1 - loss
        # 0  - a tie
        # 1  - win 
        if result=='X':
            return (-1,0,0)
        elif result=='O':
            return (1,0,0)
        elif result=='.':
            return (0,0,0)


        
        for i in range(0,3):
            for j in range(0,3):
                if self.current_state[i][j]=='.':

                    # On the empty field player 'X' makes a move and calls Max
                    # That's one branch of the game tree.
                    self.current_state[i][j]='X'

                    (m,max_i,max_j)=self.max_alpha_beta(alpha,beta)

                    # Fixing the maxv value if needed(for making the overall logic v<-Min(v,Max_Val(alpha,beta)))
                    if m<minv:
                        minv=m 
                        x=i
                        y=j 

                    # Setting back the field to empty
                    self.current_state[i][j]='.'

                    #pruning step
                    if m<=alpha:
                        return (minv,x,y)

                    #beta value setting    
                    if minv<beta:
                        beta=minv 
        return(minv,x,y)
    
    # activation function for starting alpha_beta pruning
    def play_alpha_beta(self):
        while True:

            self.draw_board()
            self.result=self.is_game_finished()

            # Printing the appropriate message if the game has ended
            if self.result!=None :
                if self.result=='X':
                    print('The Winner is X !')
                elif self.result=='O':
                    print('The Winner is O !')
                elif self.result=='.':
                    print("It's a tie")
                self.initialize_game()
                return 


            # If it's player's turn
            if self.player_turn=='X':
                while True :

                    #timer is started
                    start_time=time.time()
                    (m,x,y)=self.min_alpha_beta(-2,2)
                    end_time=time.time()

                    #Evaluation Time to get back to human with recommended move
                    print('Evaluation time is: {}sec'.format(round(end_time-start_time,7)))

                    #recommmended move
                    print('Recommended Move : X={},Y={}'.format(x,y))

                    #taking input(position) from user for inserting the value
                    x1=int(input('Insert the X coordinate: '))
                    y1=int(input('Insert the Y coordinate '))

                    x=x1
                    y=y1

                    #checking for legal_move 
                    if self.is_legal_move(x1,y1):
                        self.current_state[x1][y1]='X'
                        self.player_turn='O'
                        break 

                    #invalid moves
                    else:
                        print('The move is not valid! Try again')
            
            
            # If it's AI's turn
            else :
                (m,x,y)=self.max_alpha_beta(-2,2)
                self.current_state[x][y]='O'
                self.player_turn='X'

#initializing game object
g=Game()

#game is started
g.play_alpha_beta()