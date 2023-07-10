print("系统启动中请稍等")
import os,time,pickle,datetime
os.system("clear");print("连接数据库")
import sqlite3
连接 = sqlite3.connect('打卡数据.db')
游标 = 连接.cursor()
os.system("clear");print("连接数据库","done");time.sleep(1)
游标.execute('''\
create table if not exists 打卡日志(
    时间,
    打卡时间,
    学科
)
''')
连接.commit()
def 写入本地变量(v,filename):
    f=open(filename,'wb')          #打开或创建名叫filename的文档。
    pickle.dump(v,f)               #在文件filename中写入v
    f.close()                      #关闭文件，释放内存。
    return filename
def 读取本地变量(filename):
    try:
        f=open(filename,'rb')
        r=pickle.load(f)
        f.close()
        return r
    except EOFError:
        return ""
user=读取本地变量("user.txt")
if user=="":
    print("检测到第一次登录")
    写入本地变量(input("取一个昵称吧: "),"user.txt")
os.system("clear")
def main():
    user=读取本地变量("user.txt")
    指令=input(f"{user}: ")
    指令=指令.split()
    if len(指令)<1:
        main()
    if 指令[0]=="#开始计时#":
        os.system('clear')
        计时=读取本地变量("计时任务")
        if 计时[0]=="停止计时":
            写入本地变量([time.time(),指令[1]],"计时任务")
        else:
            print("当前有计时任务,继续需要停止之前的任务")
        main()
    elif 指令[0]=="#停止计时#":
        os.system('clear')
        计时=读取本地变量("计时任务")
        if 计时[0]!="停止计时":
            时间=time.time()-计时[0]
            写入本地变量(["停止计时"],"计时任务")
            os.system("clear");print(f'''\
    @{user} #停止计时#
        已停止计时 {计时[1]} 已学习 {时间}s''')
            print("正在结算")
            data = (f'{datetime.datetime.today()}', 时间, 计时[1])
            sql = 'insert into 打卡日志 values (?, ?, ?)'
            游标.execute(sql, data)
            连接.commit()
            print("结算完成")
        else:
            print("你还未创建任务!")
        main()
    elif 指令[0]=="#查询#":
        os.system("clear")
        计时=读取本地变量("计时任务")
        if 计时[0]!="停止计时":
            时间=time.time()-计时[0]
            print("当前任务已进行",时间,"秒")
        else:
            print("当前无任务")
        if input("需要查询之前的嘛?(Y/n)")!="n":
            sql = 'select * from 打卡日志'
            游标.execute(sql)
            for item in 游标:
                print(f'''\
日期:{item[0]}
耗时:{item[1]}
学科:{item[2]}
------------------------''')
        main()
    elif 指令[0]=="#修改用户名#":
        os.system('clear')
        if len(指令)==2:
            写入本地变量(指令[1],"user.txt")
            print("修改用户名成功!")
        else:
            print("修改用户名失败:过多或过少的参数")
        main()
    elif 指令[0]=="#帮助#":
        os.system('clear')
        print('''\
        #开始计时# 学科
        #停止计时#
        #查询#
        #修改用户名# 用户名
        ''')
        main()
    else:
        print("该指令不存在! 请输入#帮助#查询可用指令!")
        main()
if __name__=="__main__":
    main()
