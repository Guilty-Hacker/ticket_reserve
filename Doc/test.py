from time import sleep, time


def war(fun):
    def didi(*args,**kwargs):
        before = time()
        print("fun....开始运行")
        result = fun(*args,**kwargs)
        print("fun....运行结束")
        after = time()
        print("运行时间",after-before)
        return result
    return didi

@war
def play(game,le=2):
    print("小豪正在打游戏{}".format(game))
    sleep(2)
    print("游戏结束")
    return "Happy"

if __name__ == '__main__':
    result = play(game="LOL")
    print(result)


