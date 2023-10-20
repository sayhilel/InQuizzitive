import random

def getQuestion() :
    index = random.randint(0,1000)
    index = index%5
    keys = qnaMap.keys()
    keys = list(keys)
    return keys[index]

def getAnswer(ques) :
    return qnaMap[ques]

def getWrongOption(ques) :
    return wrongOptMap[ques]
    
qnaMap = {
    "Do you have to spend money to become a UGTA?": "No I don't, I get paid $1200 per course!", 
    "Will this impact my professional and academic career?":"Yes! I get to connect with my professors expanding my network and career opportunities",
    "Who can I help as UGTA?":"I get to help EVERYONE taking the course, and myself!",
    "How does being a UGTA benefit me?":"I improve my communication skills, enhance my resume, master course material, increase my networking capabilties, AND get paid",
    "Would employers care that I became a UGTA?":"My prospective employers will LOVE that I have experience teaching others as it showcases my leadership skills, collaborative thinking, and self-resiliance."
}

wrongOptMap = {
    "Do you have to spend money to become a UGTA?":"Absolutely, I have to spend $400",
    "Will this impact my professional and academic career?": "Not at all, I'm doing this out of boredom",
    "Who can I help as UGTA?":"Sadly no one, not even myself",
    "How does being a UGTA benefit me?":"Being a UGTA only benefits the students and professors not me ",
    "Would employers care that I became a UGTA?":"Nope, they only care about my GPA"
}

ques = getQuestion()
ans= getAnswer(ques)
wro = getWrongOption(ques)

print(ques, ans, wro)