from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import random

typeHeader = "[Barney Bot] "

def initialize(username, password):
    driver.get('http://koreapas.com')
    driver.find_element_by_name("user_id").clear()
    driver.find_element_by_name("user_id").send_keys(username)
    driver.find_element_by_name("password").clear()
    driver.find_element_by_name("password").send_keys(password)
    driver.find_element_by_css_selector("td > input[type=\"image\"]").click()
    driver.get('http://www.koreapas.com/bbs/talk.php?by=3')

def makeDic(**kwargs):
	l=[]
	for key in kwargs:
		l.append({'cmd':key, 'f':kwargs[key]})
	return l

def typeIn(str):
    conv = driver.find_element_by_css_selector("input.conversation")
    conv.clear()
    conv.send_keys(typeHeader + str)
    conv.send_keys(Keys.ENTER)

def howmanyUsers(*arg):
    global safetyLock
    conv = driver.find_element_by_css_selector("input.conversation")
    conv.clear()
    userList = driver.find_element_by_class_name('member_list')
    users = userList.find_elements_by_class_name('user')
    numUsers = str(len(users))
    sendStr = "현재 " + numUsers + "명의 유저가 잉여력을 발산하고 있습니다."
    typeIn(sendStr)
    safetyLock = 0

def whatUsers(*arg):
    global safetyLock
    userList = driver.find_element_by_class_name('member_list')
    sendStr = "현재 잉여인 유저들: "
    for e in userList.find_elements_by_class_name('user'):
        sendStr = sendStr + e.text + "/"
    sendStr = sendStr[:-1]
    typeIn(sendStr)
    safetyLock = 0

def attackUser(*arg):
    global safetyLock
    sendStr = ''
    n = arg[0]
    c = arg[1].replace('-attack ','')
    if (len(c) - len(c.replace(' ','')))>0:
        typeIn("명령어 오류! (형식: -attack 닉네임)")
        safetyLock = 0
        return False
    else:
        userList = driver.find_element_by_class_name('member_list')
        users = userList.find_elements_by_class_name('user')
        for el in users:
            if (el.text==c)&(c!=n):
                case = random.randint(0,4)
                critical = random.randint(0,9)
                target = c
                sendStr=n+'님이 '
                if case==0:
                    sendStr = sendStr + '두꺼운 전공서적으로 '
                elif case==1:
                    sendStr = sendStr + '거대한 솜사탕으로 '
                elif case==2:
                    sendStr = sendStr + '수중의 돈을 모두 던지며 '
                elif case==3:
                    sendStr = sendStr + '지나가는 연대생의 신발을 빼앗아 '
                elif case==4:
                    sendStr = sendStr + '고파파에게 고자질해서 '
                sendStr = sendStr + target + '님을 공격합니다.'
                typeIn(sendStr)
                if critical==9:
                    typeIn('Critical Hit! ' + target + ': 헤롱헤롱~')
                safetyLock = 0
                return True
            elif (el.text==c)&(c==n):
                sendStr=n+'님이 자신을 마구 괴롭힙니다. 변태!'
                typeIn(sendStr)
                safetyLock = 0
                return True
        sendStr=n+'님이 허공에 주먹을 마구 휘두릅니다. 휙휙!'
        typeIn(sendStr)
        safetyLock = 0
        return True

def randAttack(*arg):
    n = arg[0]
    userList = driver.find_element_by_class_name('member_list')
    users = userList.find_elements_by_class_name('user')
    target = users[(random.randint(1,len(users))-1)].text
    attackUser(n, target)
    

def randUser(*arg):
    global safetyLock
    sendStr = ''
    n = arg[0]
    userList = driver.find_element_by_class_name('member_list')
    users = userList.find_elements_by_class_name('user')
    target = users[(random.randint(1,len(users))-1)].text
    if n==target:
        sendStr = n + " 왈: 자추라니... 내가 자추라니!!!"
    else:
        sendStr = n + " 왈: 너로 정했다, " + target + "!!!"
    typeIn(sendStr)
    safetyLock = 0

def cmdHelp(*arg):
    global safetyLock
    typeIn("사용 가능한 명령어를 표시합니다.")
    typeIn("-help: 이 도움말을 표시합니다. -who: 채팅 중인 유저 목록을 띄웁니다. -count: 채팅 중인 유저의 수를 봅니다. -rand: 임의의 유저를 지목합니다. -attack NICKNAME: 해당 유저를 공격합니다. -ra: 임의의 유저를 공격합니다.")
    safetyLock = 0

def onCommand(): #to be depricated
    global safetyLock, cmdList
    safetyLock = 1
    for k in cmdList:
        if k['cmd']==cmdSet:
            print ("command "+cmdSet+" found... fire event! ")
            k['f']()
            break
        
def makeBool():
    global cmdSet, cmdList, safetyLock
    b = False
    o = driver.find_elements_by_class_name('user_conversation')[-1]
    c = o.find_element_by_class_name('cs_contents').text
    n = o.find_element_by_class_name('conversation_nick').text
    if safetyLock==0:
        for i in cmdList:
            d = ''
            if i['cmd']=='hel':
                d='-help'
            else:
                d='-'+i['cmd']
            if c==d:
                cmdSet = i['cmd']
                i['f'](n, c)
                return True
                break
            elif c.startswith('-attack '):
                cmdSet = i['cmd']
                attackUser(n, c)
                return True
                break
    return False
    
def waitCommands():
    global cmdSet, cmdList
    try:
        print ("waiting commands...")
        wait = WebDriverWait(driver, 300).until(
                lambda driver : makeBool())
        #onCommand()
    finally: 
        print('resetting the listener on command ' + cmdSet +' ...')
        cmdSet=''
        wait = None
        waitCommands()



driver = webdriver.Firefox()
cmdSet=''
cmdList=makeDic(hel=cmdHelp, who=whatUsers, count=howmanyUsers, rand=randUser, attack=attackUser, ra=randAttack)
safetyLock=0
initialize()
