import re

file1 = open('/Users/aalcedo/repos/final.txt', 'r')
Lines = file1.readlines()

dict = {}
allProjectDic = {}
outputLine = ""
projectCode = ""

# Strips the newline character
for line in Lines:
    if "----------" in line:
        allProjectDic[projectCode] = dict
        lastSlashIdx = line.rfind('/') + 1
        prev = line[lastSlashIdx:]
        firstIndexOfMinus = prev.find('---')

        projectCode = prev[:firstIndexOfMinus]
        allProjectDic[projectCode] = {}
        dict = {}

    if "@" in line:
        try:
            emails = re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", line)
            email = emails[0]

            restOfTheLine = line[line.rfind('@') + 1:]
            splits = restOfTheLine.split(",")
            insertions = int(splits[1])
            deletions = int(splits[2])
            files = int(splits[3])
            commits = 0
            if (len(splits) > 4):
                commits = int(splits[4])

            if email in dict:
                oldContributor = dict[email]
                insertions = insertions + oldContributor[0]
                deletions = deletions + oldContributor[1]
                files = files + oldContributor[2]
                commits = commits + oldContributor[3]

            dict[email] = [insertions, deletions, files, commits]
        except:
            print("An exception occurred with mail" + line)

for key in allProjectDic:
    for mail in allProjectDic[key]:
        print(key + "," + mail + "," + str(allProjectDic[key][mail][0])+ "," + str(allProjectDic[key][mail][1])+ "," + str(allProjectDic[key][mail][2])+ "," + str(allProjectDic[key][mail][3]))
