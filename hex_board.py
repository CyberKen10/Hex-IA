import copy
from utils import dfs
class HexBoard:
    def __init__(self,size:int):
        self.size=size
        self.board=[[0]*size for _ in range(size)]
        self.player_positions={1:set(),2:set()}
    def clone(self)->"HexBoard":
        cloned=self.__class__(self.size)
        cloned.board=copy.deepcopy(self.board)
        cloned.player_positions={1:copy.deepcopy(self.player_positions[1]),2:copy.deepcopy(self.player_positions[2])}
        return cloned
    def place_piece(self,row:int,col:int,player_id:int)->bool:
        if self.board[row][col]!=0:return False
        self.board[row][col]=player_id
        self.player_positions[player_id].add((row,col))
        return True
    def get_possible_moves(self)->list:
        result=[]
        for i in range(self.size):
            for j in range(self.size):
                if(self.board[i][j]==0):result.append((i,j))
        return result
    def check_connection(self,player_id:int)->bool:
        return dfs(self.player_positions[player_id],player_id,self.size)
    def is_empty(self,row:int,col:int)->bool:
        return self.board[row][col]==0
    def get_player_at(self,row:int,col:int)->int:
        return self.board[row][col]
    def print_board(self):
        space=""
        print(space,end="     ")
        for i in range(self.size):print(f"\033[31m{i}  \033[0m",end=" ")
        print("\n")
        for i in range(self.size):
            print(space,end=" ")
            print(f"\033[34m{i}  \033[0m",end=" ")
            for j in range(self.size):
                if self.board[i][j]==0:print("⬜ ",end=" ")
                if self.board[i][j]==1:print("🟦 ",end=" ")
                if self.board[i][j]==2:print("🟥 ",end=" ")
                if j==self.size-1:print(f"\033[34m {i} \033[0m",end=" ")
            space+="  "
            print("\n")
        print(space,end="    ")
        for i in range(self.size):print(f"\033[31m{i}  \033[0m",end=" ")







