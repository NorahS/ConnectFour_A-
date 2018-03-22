### AI Project - MiniMax ConnectFour
### Fall'17, PSU  Dana AlHenaki and Norah ALsabti
###Main.py Runs the game

from Game import ConnectFour
from AlphaBeta import *
import sys
from Tkinter import *
from Util import *


############################################### constants
R = 55 
x = 40
y = 30
width = 600
height = 380
limits =[y+(5*R)+2]*7
turns=["#E0F288","#16243F"]
playes =[]

############################################## Logic 
def get_input():
     global human_input
     col = human_input
     human_input = None
     return (col,"")

def newGame():
     global game
     global turn
     global GameOver
     global limits
     global playes
     global Human
     global human_input
     Human = True ## ->  starts first
     human_input = None
     game = ConnectFour()
     turn = 0
     GameOver = False
     limits =[y+(5*R)+2]*7
     playes = []
     run.info(" ")

#### Game Vars
game =  ConnectFour()
turn = 0 ## -> Human starts 
Human = True ## ->  starts first
GameOver = False
human_input = None
HumanId = 0  ##->  fixed

############################################## Players agent
alphabeta_player = lambda :alpha_beta_search(game,depth=5,eval_fn=focused_evaluate) 
alphabeta_player2 = lambda :alpha_beta_search(game,depth=6,eval_fn=better_evaluate)  ##depth 6
ab_iterative_player = lambda :run_search_function(game,search_fn=alpha_beta_search,eval_fn=focused_evaluate, timeout=5) ## Variable Ddepth

##fixed depth
callBack =[get_input,alphabeta_player]
#callBack =[ get_input,alphabeta_player2]

#to play  ID uncomment
#callBack =[ get_input,ab_iterative_player]

############################################# Interface

def get_move(event):
        global human_input 
        if (event.x>=40 and event.x<=(8*R)-0):
             col = ((event.x-40)/R)%7
             if limits[col]<=30:
                  return
             human_input = col

def human_callback(event):
     if Human and not GameOver:
          get_move(event)
         
          
def restart_program(event):
    for token in playes:
         run.deleteTokens(token)
    newGame()



class Board(Frame):

    
     def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.canv= Canvas(master, width=width, height=height)
        self.canv.pack()
        self.createBoard()
        self.canv.bind("<Button-1>",  human_callback)
        self.restartImage = PhotoImage(file="Restart.gif")
        self.label = Label(self.canv,image=self.restartImage)
        self.label.place(x=450,y=110)
        self.label.bind("<Button-1>", restart_program)
        self.winfo_toplevel().title("Connect Four")
        self.debug_inf= self.canv.create_text(520,250,fill="#C71E3C", font="Helvatica 12 bold",text="")
        
     def createBoard(self):
          x=40
          y=30
          self.canv.create_line(x+(R*0),y,x+(R*0), y+6*R, fill="#4A667C", width="2.5")
          for i in range(1,7):
               self.canv.create_line(x+(R*i),y,x+(R*i), y+6*R, fill="#88A1B5", width="2", dash=(2,2))
          self.canv.create_line(x+(R*7),y,x+(R*7), y+6*R, fill="#4A667C", width="2.5")
          for i in range(1,6):
               self.canv.create_line(x,y+(R*i),x+7*R, y+(R*i), fill="#88A1B5", width="2" , dash=(2,2))
          self.canv.create_line(x,y+(R*6),x+7*R, y+(R*6), fill="#4A667C", width="2.5")

     def draw(self,col):
          global Human
          d= R-10
          start = x+5
          ball = self.canv.create_oval(start+(d*col)+(10*col),0,(start+(d*col)+(10*col)+d),d,fill=turns[turn], outline=turns[turn])
          playes.append(ball)
          while(limits[col]>self.canv.coords(ball)[1]):
                  self.canv.move(ball,0,2) 
          limits[col]-=R
          Human = not Human
     def deleteTokens(self,token):
          self.canv.delete(token)
     def win(self, string):
          text= self.canv.create_text(235,200,fill="#C71E3C", font="Helvatica 40 bold",text=string)
          playes.append(text)
          
     def info(self,string):
         if string == "":
               return
         self.canv.itemconfigure(self.debug_inf,text=string)

     

########################################### RUNNING
root=Tk()
run = Board(master=root)

while True:
     while(not game.gameOver()):
          GameOver = False
          col = None
          while col == None:
               try:
                    run.update()
               except TclError:
                    sys.exit(0) 
               colT = callBack[turn]()
               col = colT[0]
               run.info(str(colT[1]))
          game.move(col)
          run.draw(col)
          run.update_idletasks()
          if game.won():
               if game.getPlayerId() == HumanId:
                   run.win("YOU HAVE WON!")
               else:
                    run.win("YOU HAVE LOST!")
          game.next_player()
          turn = game.getPlayerId()
     try:
          run.update()
     except TclError:
            sys.exit(0)
     GameOver = True
     
