#八数码问题
#使用A*启发式搜索算法
#h(n)=P(n)+3S(n)
#yanghao 20172131139

import copy
import time

#目标状态
goal_state = [[1,2,3],
             [4,5,6],
             [7,8,0]]
#open表
open_state = []
#close表
close_state = []

#棋盘类
class Board:
    curList = []
    preList = []
    Cost = 0
    goalstate=[]
    #构造函数
    def __init__(self, list = [], prelist = [], cost = 0):
        self.curList = list
        self.preList = prelist
        self.Cost = cost
        for i in range(len(goal_state)):
            self.goalstate+=goal_state[i]

    #设置棋盘的上一个状态，cost值稍后更新
    def SetPre(self, newPreList):
        self.preList = newPreList
        self.Cost = newPreList.mycost

    #判断两个棋盘是否相同
    def IsSame(self, struNum1):
        if self.curList == struNum1.curList:
            return True
        else:
            return False

    #在open表中获取棋盘的前一个状态
    def GetItsPre(self):
        global close_state
        for i in range(len(close_state)):
            if self.preList == close_state[i].curList:
                return close_state[i]

    #获取棋盘中0(空格)的位置
    def GetZeroIndex(self):
        for i in range(len(self.curList)):
            for j in range(len(self.curList[i])):
                if self.curList[i][j] == 0:
                    return [i,j]

    #获取当前状态在某个列表中的位置
    def GetListIndex(self, someList):
        for i in range(len(someList)):
            if self.curList == someList[i].curList:
                return i
        return -1

    #获取目标状态某个数字的位置
    def GetGoalIndex(self,number):
        global goal_state
        for i in range(len(goal_state)):
            for j in range(len(goal_state)):
                if number==goal_state[i][j]:
                    return i,j

    #对节点n中将牌排列顺序的计分,判断两个数字的顺序是否与目标状态一致
    def GetOrder(self,number1,number2):
        global goal_state
        coor1=self.GetGoalIndex(number1)#第一个数的坐标
        coor2=self.GetGoalIndex(number2)#后继者的坐标
        if coor1[0]<coor2[0]:
            return True
        elif coor1[0] == coor2[0]:
            if coor1[1]<coor2[1]:
                return True
            else:
                return False
        elif coor1[0]>coor2[0]:
            return False
    
    #判断两个数字的顺序是否与目标状态一致
    def getScore(self,somelist):
        temp=[]
        for i in range(len(somelist)):
            temp+=somelist[i]
        for i in range(len(temp)):
            if self.goalstate.index(temp[i]) <self.goalstate.index(temp[(i+1)%9]):
                return True
            else:
                return False
        
    #获取到目标节点的耗散值
    #h(n)=P(n)+3S(n)
    def GetGoalCost(self):
        pn = 0 
        sn = 0
        coordinate=(0,0)
        for i in range(len(self.curList)):
            for j in range(len(self.curList[i])):
                if self.curList[i][j]==0:
                    pass#为0是为空格，没有将牌
                else:
                    coordinate=self.GetGoalIndex(self.curList[i][j])
                #计算每一个将牌位与目标之间的曼哈顿距离
                #h(n)=P(n)
                pn+=abs(coordinate[0]-i)+abs(coordinate[1]-j)       
        for i in range(len(self.curList)):
            for j in range(len(self.curList[i])):
                if i==1 and j==1:
                    #中心位置
                    if self.curList[i][j]==0:
                        pass#无将牌估分取0
                    else:
                        sn+=1#有将牌估分取1
                else:
                    if self.getScore(self.curList):
                        pass#一致估分取0
                    else:
                        sn+=2#不一致估分取2

        return pn+3*sn
    
#指定排序的key参数
def searchKey(elem):
    return elem.Cost

#判断目标是否可达
def checkNoAns(list):
    sum = 0
    for i in range(0, len(list), 1):
        for j in range(0, len(list[i]), 1):
            for ii in range(0, i, 1):
                for jj in range(0, len(list[i]), 1):
                    if list[ii][jj] != 0 and list[i][j] != 0 and list[ii][jj] < list[i][j]:
                        sum += 1
            for jj in range(0, j, 1):
                if list[i][jj] != 0 and list[i][j] != 0 and list[i][jj] < list[i][j]:
                    sum += 1
    if sum % 2 == 0:
        return True
    else:
        return False

#解决八数码问题
def eight_puzzle(curList):
    startNum = Board(curList, [], 0)
    open_state.append(startNum)
    startTime = time.time()
    while(open_state != []):
        nowNum = open_state[0]
        open_state.remove(nowNum)    #从队列头移除
        close_state.append(nowNum)    #添加到已读队列
        if nowNum.curList == goal_state:
            print("成功找到解：")
            while(nowNum.preList != []):
                for i in nowNum.curList:
                    print(i)
                print('')                   
                nowNum = nowNum.GetItsPre()#回到上一个状态
            for i in nowNum.curList:
                    print(i)
            break
        else:
            [idx, jdx] = nowNum.GetZeroIndex()
            #将空格上移
            if idx - 1 >= 0:
                upList = copy.deepcopy(nowNum.curList)
                upList[idx][jdx] = upList[idx - 1][jdx]
                upList[idx - 1][jdx] = 0
                upNum = Board(upList, nowNum.curList, nowNum.Cost + 1)
                #A*算法：代价 = 到达此状态代价 + 期望到达目标节点代价
                upNum.Cost += upNum.GetGoalCost()
                #如果新节点没有被走过
                if upNum.GetListIndex(close_state) == -1:
                    tmpIndex = upNum.GetListIndex(open_state)
                    if tmpIndex != -1:
                        #当新节点已经出现在未读队列中，如果新节点的代价更小，则更新，否则不更新
                        if upNum.Cost < open_state[tmpIndex].Cost:
                            open_state.remove(open_state[tmpIndex])
                            open_state.append(upNum)
                    else:
                        open_state.append(upNum)
            #将空格下移
            if idx + 1 < 3:
                downList = copy.deepcopy(nowNum.curList)
                downList[idx][jdx] = downList[idx + 1][jdx]
                downList[idx + 1][jdx] = 0
                downNum = Board(downList, nowNum.curList, nowNum.Cost + 1)
                downNum.Cost += downNum.GetGoalCost()
                # 如果新节点没有被走过
                if downNum.GetListIndex(close_state) == -1:
                    tmpIndex = downNum.GetListIndex(open_state)
                    if tmpIndex != -1:
                        # 当新节点已经出现在未读队列中，如果新节点的代价更小，则更新，否则不更新
                        if downNum.Cost < open_state[tmpIndex].Cost:
                            open_state.remove(open_state[tmpIndex])
                            open_state.append(downNum)
                    else:
                        open_state.append(downNum)
            #将空格左移
            if jdx - 1 >= 0:
                leftList = copy.deepcopy(nowNum.curList)
                leftList[idx][jdx] = leftList[idx][jdx - 1]
                leftList[idx][jdx - 1] = 0
                leftNum = Board(leftList, nowNum.curList, nowNum.Cost + 1)
                leftNum.Cost += leftNum.GetGoalCost()
                # 如果新节点没有被走过
                if leftNum.GetListIndex(close_state) == -1:
                    tmpIndex = leftNum.GetListIndex(open_state)
                    if tmpIndex != -1:
                        # 当新节点已经出现在未读队列中，如果新节点的代价更小，则更新，否则不更新
                        if leftNum.Cost < open_state[tmpIndex].Cost:
                            open_state.remove(open_state[tmpIndex])
                            open_state.append(leftNum)
                    else:
                        open_state.append(leftNum)
            #将空格右移
            if jdx + 1 < 3:
                rightList = copy.deepcopy(nowNum.curList)
                rightList[idx][jdx] = rightList[idx][jdx + 1]
                rightList[idx][jdx + 1] = 0
                rightNum = Board(rightList, nowNum.curList, nowNum.Cost + 1)
                rightNum.Cost += rightNum.GetGoalCost()
                # 如果新节点没有被走过
                if rightNum.GetListIndex(close_state) == -1:
                    tmpIndex = rightNum.GetListIndex(open_state)
                    if tmpIndex != -1:
                        # 当新节点已经出现在未读队列中，如果新节点的代价更小，则更新，否则不更新
                        if rightNum.Cost < open_state[tmpIndex].Cost:
                            open_state.remove(open_state[tmpIndex])
                            open_state.append(rightNum)
                    else:
                        open_state.append(rightNum)

            #按照COST排序
            open_state.sort(key=searchKey)
    endTime = time.time()
    print("所用时间 = %.3fs" %(endTime - startTime))

#main函数
if __name__ == "__main__":
    #定义初始状态
    current_state = [[1,3,4],
                    [2,8,6],
                    [5,7,0]]
    print('初始状态：')
    for i in range(len(current_state)):
        print(current_state[i])
    print('目标状态：')
    for i in range(len(goal_state)):
        print(goal_state[i])
    #判断是否可达
    if(checkNoAns(goal_state) == False):
        print("目标不可达！")
        exit(1)
    else:
        print('目标可达，开始求解')
    #开始求解
    eight_puzzle(current_state)
    time.sleep(3)