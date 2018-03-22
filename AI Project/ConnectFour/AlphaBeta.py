### AI Project - MiniMax ConnectFour
### Fall'17, PSU  Dana AlHenaki and Norah ALsabti
###AlphaBeta procedures 


from Game import ConnectFour
from evaluationFunctions import *

INFINITY = float("infinity")
NEG_INFINITY = float("-infinity")

def get_all_next_moves(board):
    for i in xrange(7):
        if board.validMove(i):
            newboard = board.clone()
            newboard.move(i)
            newboard.won()
            newboard.next_player()
            yield (i, newboard)
        else:
            pass



def is_terminal(depth, board):
    """
    Generic terminal state check, true when maximum depth is reached or
    the game has ended.
    """
    return depth <= 0 or board.gameOver()


def alpha_beta_search(board, depth,
                      eval_fn,
                      # NOTE: You should use get_next_moves_fn when generating
                      # next board configurations, and is_terminal_fn when
                      # checking game termination.
                      # The default functions set here will work
                      # for connect_four.
                      get_next_moves_fn=get_all_next_moves,
		      is_terminal_fn=is_terminal):

    
    a = NEG_INFINITY #alpha
    b = INFINITY      #beta
    best_Sval = None
    for move,new_board in get_next_moves_fn(board):
        val =  -1*alpha_beta_search_recursive(new_board, depth-1,a,b,False,eval_fn, get_next_moves_fn, is_terminal_fn)
        if  best_Sval == None or best_Sval[1] < val:
            best_Sval = (move,val)
        if a < best_Sval[1]:
            a = best_Sval[1]
       
    info= "ALPHA-BETA:\n   Decided on column "+str(best_Sval[0])+ "\n   with rating "+ str(best_Sval[1])
    return (best_Sval[0],info)


def alpha_beta_search_recursive(board,depth,a,b,turn_max,eval_fn,get_next_moves_fn =get_all_next_moves,is_terminal_fn=is_terminal):

    if is_terminal_fn(depth, board):
        return eval_fn(board)
    
    best_Sval = None

 
    for move,new_board in get_next_moves_fn(board):
        val = -1* alpha_beta_search_recursive(new_board, depth-1,a,b,not turn_max,eval_fn, get_next_moves_fn, is_terminal_fn)

        if best_Sval == None or val > best_Sval:
            best_Sval = val
        if turn_max:
            if a < best_Sval:
                a = best_Sval
        else:
            if b >(-1*best_Sval):
                b =(best_Sval*-1)
        if a>b:
             return  best_Sval

   
    return best_Sval




