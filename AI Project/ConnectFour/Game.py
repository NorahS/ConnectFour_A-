### AI Project - MiniMax ConnectFour
### Fall'17, PSU  Dana AlHenaki and Norah ALsabti
###ConnectFour class  




class ConnectFour(object):
    # array implemenation for now
    
    def __init__(self, board_array = None,   currentPlayer = None, tokens=0):
        if board_array == None:
            self.board =[]
            for i in range(7):
                self.board.append([])
        else:
            self.board = board_array

        if currentPlayer == None:
            self.currentPlayer = 0
        else:
            self.currentPlayer = currentPlayer
        self.Winner = -1
        self.tokens = tokens
            
    def validMove(self,col):
        return not (len(self.board[col])==6)
            

    def getPlayerId(self):
        return  self.currentPlayer
    
    def move(self,col):
        self.board[col].append(self.currentPlayer)
        self.tokens+=1

    def next_player(self):
          self.currentPlayer =(self.currentPlayer+1)%2

          
    def won(self):
        if self.checkCol(self.currentPlayer):
            return True
        if self.checkRow(self.currentPlayer):
            return True
        return self.checkDiognal( self.currentPlayer)
    
    def gameOver(self):
        if self.Winner != -1 :
            return  True
        
        for col in self.board:
            if len(col) < 6:
                return False

        return True


    def checkCol(self,playerId):
        winnerId = str([playerId]*4)[1:-1] 
        for col in self.board:
            colstr = str(col)[1:-1]
            if winnerId in colstr:
                self.Winner = playerId
                return True
        return False
    

    def checkRow(self,playerId):
           list1 = [str(playerId)]*4
           winnerId = "".join(list1) 
           for row in range(6): ##rows
               rowstr=""
               for col in self.board:
                   if len(col)>row:
                       rowstr+=str(col[row])
                   else:
                       rowstr+=" "
               if str(winnerId) in rowstr:
                    self.Winner = playerId
                    return True
           return False
        

    def checkDiognal(self, playerId):
        list1 = [str(playerId)]*4
        winnerId = "".join(list1)
        for i in [5,4,3]:
            for col in range(len(self.board)):
                c=i
                r=col
                strr=""
                while(r<7  and c>=0 ):
                    leng = len(self.board[r]) 
                    if (leng == 0):
                        strr+="-"
                    elif c < leng :
                         strr+=str(self.board[r][c])
                    else:
                       strr+="-"  
                    c-=1
                    r+=1
                if winnerId  in strr:
                    self.Winner = playerId
                    return True
        for i in [0,1,2]:
            for col in range(len(self.board)):
                c=i
                r=col
                strr=""
                while(r<7  and c<6 ):
                    leng = len(self.board[r]) 
                    if (leng == 0):
                        strr+="-"
                    elif c < leng :
                         strr+=str(self.board[r][c])
                    else:
                       strr+="-"  
                    c+=1
                    r+=1
                if winnerId in strr:
                    self.Winner = playerId
                    return True
                             
    def getCell(self, row, col):
        if row< len(self.board[col]):
            return self.board[col][row]
        else :
            return "_"

    def clone(self):
        b=[]
        for i in self.board:
            b.append(list(i))
        return   ConnectFour( board_array = b,currentPlayer= self.currentPlayer,tokens=self.tokens )


    def longest_chain(self,PlayerId):
        maxString = 0
        for i in [3,2,1]:
            if self.checkColLength(PlayerId,i):
                maxString = i
                break;
            elif self.checkRowLength(PlayerId,i):
                maxString = i
                break
        if maxString == 3:
            return maxString
         
        return max(maxString, self.checkDiognalLength(PlayerId))

    def checkColLength(self,playerId, length):
        winnerId = str([playerId]*length)[1:-1] 
        for col in self.board:
            colstr = str(col)[1:-1]
            if winnerId in colstr:
                return True
        return False

    def checkRowLength(self,playerId, length):
           list1 = [str(playerId)]*length
           winnerId = "".join(list1) 
           for row in range(6): ##rows
               rowstr=""
               for col in self.board:
                   if len(col)>row:
                       rowstr+=str(col[row])
                   else:
                       rowstr+=" "
               if str(winnerId) in rowstr:
                    return True
           return False

    def checkDiognalLength(self,PlayerId):
           maxTokens = 0
           for col in range(7):
               for  row in range(len(self.board[col])):
                   token = self.board[col][row]
                   if token != PlayerId:
                       break  #go to the next token
                   for i in [1,2]:   #Forward
                       try:
                           if self.board[col+i][row+i] == token:
                               maxTokens = i+1
                           else:
                               break;
                           
                       except IndexError:
                           break
                   if maxTokens == 3:
                        return maxTokens
                    
                 
                   for i in [1,2]:   #Backward
                       try:   
                           if col > 0 and row > 0 and self.board[col-i][row-i] == token:
                               maxTokens = i+1
        
                           else :
                               break;
                           
                       except IndexError:
                           break
                  
           return maxTokens
                    
    def get_OtherPlayerId(self):
           if self.currentPlayer == 0:
               return 1
           return 0
       
    def get_winner(self):
        return self.Winner
    
    def num_tokens_on_board(self):
        return self.tokens
    
    def get_height_of_column(self ,col):
        return len(self.board[col])

    def get_top_elt_in_column(self, col): ## col should not be empty

        return int(self.board[col][-1])
    def __str__(self):
        """ Return a string representation of this board """
        s = ""
        for i in reversed(range(6)):
            for j in range(7):
                if len(self.board[j]) > i:
                    s+= str(self.board[j][i])+" "
                else:
                    s+="_ "
            s+="\n"
        return s
