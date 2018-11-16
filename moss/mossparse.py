import re
import csv
COMP_STR = '<TR><TD><A HREF="(.*?)">submissions\/(.*?)\/main\.py \((.*?)\)<\/A>[\s\n\r]*?<TD><A HREF="(.*?)">submissions\/(.*?)\/main\.py \((.*?)\)<\/A>[\s\n]*?<TD ALIGN=right>(\d*)'
COMP_PAT = re.compile(COMP_STR)
PARTNER_STR = '#\s*?partner-login:\s*?(\w*)\n'
PARTNER_PAT = re.compile(PARTNER_STR)
UB = 40

VERIFIED = 'Verified'
UNKNOWN = 'Unknown'
SUSPICIOUS = 'Suspicious'
INVALID_USER = ['test-tyler', 'szou28', 'tharter']

class StudentInfo:
    def __init__(self, url, user, sim, simUser):
        self.user = user
        self.sim = {simUser: (url, sim)}
        self.partner = self.findPartner()

    def update(self, url, sim, simUser):
        self.sim[simUser] = (url, sim)

    def findPartner(self):
        with open("submissions/{netid}/main.py".format(netid=self.user), 'rU') as fr:
            code = fr.read()
            partners = PARTNER_PAT.findall(code)
            if len(partners) > 0:
                return partners[0]
            else:
                return None

    def pprint(self):
        print("student id: {id}, sim: {sim}, partner: {partner}".format(
            id = self.user, sim = self.sim, partner = self.partner))

class StudentInfoMgr:
    def __init__(self):
        self.stuPool = {}

    def addStudentInfo(self, url, user, sim, simUser):
        if user in INVALID_USER or simUser in INVALID_USER:
            return False
        if user in self.stuPool:
            self.stuPool[user].update(url, sim, simUser)
        else:
            self.stuPool[user] = StudentInfo(url, user, sim, simUser)
        return True

    def get(self, user):
        return self.stuPool[user]

    def verifyPartner(self, user1, user2):
        user1Partner = self.get(user1).partner
        user2Partner = self.get(user2).partner
        if user1Partner and user2Partner:
            if user1Partner == user2 and user2Partner == user1:
                return user1Partner, user2Partner, VERIFIED
            else:
                return user1Partner, user2Partner, SUSPICIOUS
        elif user1Partner == None and user2Partner == None:
            return user1Partner, user2Partner, UNKNOWN
        else:
            if user1Partner == user2 or user2Partner == user1:
                return user1Partner, user2Partner, VERIFIED
            else:
                return user1Partner, user2Partner, SUSPICIOUS

mgr = StudentInfoMgr()

class MossMatch:
    def __init__(self, url1, user1, sim1, url2, user2, sim2, lineMatched):
        self.stu1 = user1
        self.stu2 = user2
        sim1 = int(sim1.replace('%',''))
        sim2 = int(sim2.replace('%',''))
        self.isSuspicious = sim1 >= UB and sim2 >= UB
        self.isValid = self.isSuspicious and mgr.addStudentInfo(url1, user1, sim1, user2) and mgr.addStudentInfo(url2, user2, sim2, user1)
        self.lineMatched = lineMatched

def readHtml(htmlFile):
    allMatches = []
    f = open("mossreport.html",'r')
    source = f.read()
    res = COMP_PAT.findall(source)
    for x in res:
        match = MossMatch(x[0], x[1], x[2], x[3], x[4], x[5], x[6])
        allMatches.append(match)
    return allMatches

def findFather(uf, userId):
    # print('stu: {id}, father: {father}'.format(id=stu.user, father=stu.father))
    if userId not in uf:
        return userId
    curFather = uf[userId]
    if curFather == userId:
        return userId
    father = findFather(uf, curFather)
    uf[userId] = father
    return father

def unionFind(allMatches):
    uf = {}
    res = {}
    idx = 0
    for match in allMatches:
        if match.isValid:
            stu1 = match.stu1
            stu2 = match.stu2
            idx += 1
            # print("{0}: stu1: {1}, stu2: {2}".format(idx, stu1, stu2))
            if stu1 not in uf and stu2 not in uf:
                uf[stu1] = stu1
                uf[stu2] = stu1
            elif stu1 in uf and stu2 in uf:
                stu1Father = findFather(uf, stu1)
                stu2Father = findFather(uf, stu2)
                uf[stu1Father] = stu2Father
            else:
                if stu1 not in uf:
                    stu2Father = findFather(uf, stu2)
                    uf[stu1] = stu2Father
                else:
                    stu1Father = findFather(uf, stu1)
                    uf[stu2] = stu1Father
    for userId in uf:
        father = findFather(uf, userId)
        if father not in res:
            res[father] = []
        res[father].append(userId)
    return res

def getResult():
    print('# CS 301 Moss Report (LB = {lb}%)'.format(lb = UB))
    matches = readHtml('mossreport.html')
    ufResult = unionFind(matches)
    unknownList = []
    collectedRes = {}
    for father in ufResult:
        l = len(ufResult[father])
        partnerVer = SUSPICIOUS
        if l == 2:
            stu1 = ufResult[father][0]
            stu2 = ufResult[father][1]
            partner1, partner2, partnerVer = mgr.verifyPartner(stu1, stu2)
            if partnerVer == VERIFIED:
                continue
            if partnerVer == UNKNOWN:
                unknownList.extend(ufResult[father])
        if partnerVer not in collectedRes:
            collectedRes[partnerVer] = {}
        if l not in collectedRes[partnerVer]:
            collectedRes[partnerVer][l] = []
        collectedRes[partnerVer][l].append(father)

    for partnerStatus in collectedRes:
        res = collectedRes[partnerStatus]
        orderedRes = sorted(res.keys())
        print("## {status} Cases".format(status=partnerStatus))
        for key in orderedRes:
            fatherList = res[key]
            print("### Groups With Size = {}".format(key))
            groupi = 0
            for father in fatherList:
                groupi += 1
                print("**Group {index}**".format(index=groupi))
                print()
                i = 0
                ufResult[father].sort()
                for stuId in ufResult[father]:
                    i += 1
                    usr = mgr.get(stuId)
                    print("{index}. **{id}** (partner: {partner}) [mailto](mailto:{id}@wisc.edu)".format(index=i, id=usr.user, partner=usr.partner))
                    for stuId2 in ufResult[father]:
                        if stuId2 in usr.sim and stuId2 > stuId:
                            print("    * {userId}, similarity: {sim} [link]({link})".format(
                                userId=stuId2, sim=usr.sim[stuId2][1], link=usr.sim[stuId2][0]))
                print()
                print("**comment**:")
                print()
                print("<hr>")
                print()
            print()
    return unknownList

getResult()
