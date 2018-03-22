### AI Project - MiniMax ConnectFour
### Fall'17, PSU  Dana AlHenaki and Norah ALsabti
### 2 Evaluation Functions  


from Game import ConnectFour


def focused_evaluate(board):
    """
    Given a board, return a numeric rating of how good
    that board is for the current player.
    A return value >= 1000 means that the current player has won;
    a return value <= -1000 means that the current player has lost
    """  
    score = 0
    if board.get_winner() == board.getPlayerId():
        score = 1210 - 5*board.num_tokens_on_board()
    elif board.get_winner() == board.get_OtherPlayerId():
        score = -1210 + 5*board.num_tokens_on_board()

    else:
         score = board.longest_chain(board.getPlayerId()) * 10
        # Prefer having your pieces in the center of the board.
         for row in range(6):
            for col in range(7):
                if board.getCell(row, col) == board.getPlayerId():
                    score -= abs(3-col)
                elif board.getCell(row, col) == board.get_OtherPlayerId(): 
                    score += abs(3-col)

    return score


def better_evaluate(board):
    """
    Given a board, return a numeric rating of how good
    that board is for the current player.
    This function is implemented based on the following paper:
	    http://www.jennylam.cc/assets/pdf/connectk.pdf 
    and another Document provided in the main folder

    """  
    score = 0
    if board.get_winner() == board.getPlayerId():
        score = 1210 - 5*board.num_tokens_on_board()
    elif board.get_winner() == board.get_OtherPlayerId():
        score = -1210 + 5*board.num_tokens_on_board()
    else:
        col_lines = int(col_threats(board))
        row_lines = int(row_threats(board))
        diagonal_lines = int(diagonal_threats(board))

        score = diagonal_lines + col_lines + row_lines

    return score


def  col_threats(board):
    danger =0
    threat = board.get_OtherPlayerId()
    
    for i in range(7):
       height = board.get_height_of_column(i) ## only lookup the top 3 tokens
       if height == 0 or height ==6:
           continue
       top = board.get_top_elt_in_column(i) ## only player at the top has a chance of wiining this line
       count = 1
       for d in [2,3]:
           if  height-d >= 0 and board.getCell(height-d, i) == top:
               count+=1
           else:
               break
       if top == threat:
           score = (count/3.0)*100
           score*=-1
       else:
           score = (count/3.0)*50 ##Defensive strategy
       danger+=score
       
    return danger

def row_threats(board):
    empty_row = 7
    for i in range(7):
        empty_row = min(empty_row ,board.get_height_of_column(i)) ##Min

    foe = board.get_OtherPlayerId()
    danger = 0
    
    danger+=6*empty_row 
    for  row in range(empty_row,6):
        for i in range(4):
            threat = 0
            neutral = 0
            steps= 0
            for j in range(4):
                token = board.getCell(row, i+j)
                if token == foe:
                    threat+=1
                elif token == "_":
                    neutral+=1
                    if board.get_height_of_column(i+j) < row:
                        steps+= row - board.get_height_of_column(i+j)
            if threat > 0 and threat+neutral == 4: ##Threat
                danger+=((threat/3.0)*-100) +(steps) 
            elif threat > 0: ##blocked ++
                if neutral == 0:
                    danger +=6
                else:
                    danger+=11
            elif neutral < 4: ##good
                danger+=(((4-neutral)/3.0)*50)
          
    return danger

def diagonal_threats(board):
    danger = 0
    foe = board.get_OtherPlayerId()
                             
    for col in range(4):
         for row in [0,1,2]: ## Check
             threat = 0
             neutral = 0
             for i in range(4):
                 token = board.getCell(row+i, col+i)
                 if token == foe:
                     threat+=1
                 elif token == "_":
                     neutral+=1

             if threat > 0 and threat + neutral == 4: ##Threat
                 danger+= ((threat/3.0)*-100)
             elif threat > 0:
                 if neutral == 0:   ##line is blocked
                     danger+=6
                 else:
                     danger+=11
             elif neutral < 4: ##possible winning line 
                 danger+=(((4-neutral)/3.0)*50)
  

    for col in [6,5,4,3]:
         for row in [0,1,2]:
             threat = 0
             neutral = 0
             for i in range(4):
                 token =board.getCell(row+i, col-i)
                 if token == foe:
                     threat+=1
                 elif token == "_":
                     neutral+=1
 
             if  threat > 0 and threat + neutral == 4: ##Threat
                 danger+= ((threat/3.0)*-100)
             elif threat > 0:
                 if neutral == 0:   ##line is blocked
                     danger+=6
                 else:
                     danger+=11
             elif neutral < 4: ##possible winning line 
                 danger+=(((4-neutral)/3.0)*50)
    return danger
