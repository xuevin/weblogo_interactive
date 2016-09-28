import math

aaLookup = "ACDEFGHIKLMNPQRSTVWY"
allMySequences = open("/home/vxue/sketchbook/logoPython/data/processing_logo.txt",'r').readlines()
mySequences = allMySequences
logoWidth = 100
myX = 0
storedKey = ""
colorIndex = 0 
fileIndex = 0 
mouseIndex = 0
currentLoopPosition =0
loopIncrement=10
largeFont = createFont("Courier", 30)
smallFont = createFont("Courier", 10)



colorMapping = dict()
for i in 'RKDENQ':
    colorMapping[i]=color(0,0,255)
for i in 'SGHTAP':
    colorMapping[i]=color(0,255,0)
for i in 'YVMCLFIW':
    colorMapping[i]=color(0)


def getTally(sequences):
    myArray=[]
    for j in range(19):
        myPosArray = []
        for i in range(len(aaLookup)):
            myPosArray.append(0)
        myArray.append(myPosArray)
            
    for each in sequences:
        for i in range(19):
            myArray[i][aaLookup.index(each[i])]+=1
    
    for i in range(19):
        for j in range(20):
            myArray[i][j]=float(myArray[i][j])/float(len(sequences)) 
    return myArray

def calculateMI(site1Index, site2Index):
    site1 = []
    site2 = []
    
    for each in mySequences[int(myX):int(myX+logoWidth)]:
        site1.append(each[site1Index])
        site2.append(each[site2Index])
    
    mutInfo = 0
    letters=set(site1+site2)
    
    # First iterate through the length of the column to find counts of all pairs
    counts=dict()
    for each in range(len(site1)):
        counts[(site1[each],site2[each])]=counts.get((site1[each],site2[each]),0)+1

    mylength = len(site1)
    for each in letters: #iterate through the letters observed at either site. If it is only observed in one site, P(A,B) = 0
        for each2 in letters: 
            numerator = (float(counts.get((each,each2),0))/mylength) # P(A,B)
            denominator= float(site1.count(each))/mylength * float(site2.count(each2))/mylength # P(A)P(B)
#            print each, each2, numerator,denominator
            if(denominator!=0 and numerator!=0):
                mutInfo+= numerator * math.log(numerator/denominator,2)
    return mutInfo


def calculateMIBatch(listOfPositions):
    
    allCounts = dict()
    for i in range(len(listOfPositions)):        
        allCounts[listOfPositions[i]]=[]
    
    
    for each in mySequences[int(myX):int(myX+logoWidth)]:
        for i in range(len(listOfPositions)):
            allCounts[listOfPositions[i]].append(each[listOfPositions[i]])

                
    allMIScores = dict()
    
    for i in range(len(listOfPositions)):
        for j in range(1,len(listOfPositions)):
            site1 = allCounts[listOfPositions[i]]
            site2 = allCounts[listOfPositions[j]]
            
            mutInfo = 0
            letters=set(site1+site2)
            
            # First iterate through the length of the column to find counts of all pairs and singles
            counts=dict()
            for each in range(len(site1)):
                counts[(site1[each],site2[each])]=counts.get((site1[each],site2[each]),0)+1
        
            mylength = len(site1)
            for each in letters: #iterate through the letters observed at either site. If it is only observed in one site, P(A,B) = 0
                for each2 in letters: 
                    numerator = (float(counts.get((each,each2),0))/mylength) # P(A,B)
                    denominator= float(site1.count(each))/mylength * float(site2.count(each2))/mylength # P(A)P(B)
        #            print each, each2, numerator,denominator
                    if(denominator!=0 and numerator!=0):
                        mutInfo+= numerator * math.log(numerator/denominator,2)
                        
            allMIScores[(i,j)]=mutInfo
            
    return allMIScores


#print getTally(mySequences[0:10])

def setup():
    size(1300, 400)
    background(255)
    # Create the font
    textFont(largeFont)
    textAlign(CENTER, TOP)
    frameRate(15)


def draw():

    background(255)
    drawLogo()
    drawLegend()
    drawScale()
    drawStoredKey()
    updateLoopPosition()
    drawMIGrid()

def drawMIGrid():
    textFont(smallFont)
    ellipseMode(CENTER);
    
    positionsOfInterest = [6,10,11,13,15,17]
    batchMI = calculateMIBatch(positionsOfInterest)
    
    offsetX = 100
    offsetY = 250
    gridSize = 20
    
    for i in range(len(positionsOfInterest)):
        text(str(positionsOfInterest[i]),offsetX + 10 + i*gridSize , offsetY)
        text(str(positionsOfInterest[i]),offsetX-10,offsetY +20 + i*gridSize )
        for j in range(i+1,len(positionsOfInterest)):
            #rect(offsetX + i*gridSize, offsetY + j*gridSize, gridSize,gridSize)
            miValue =  batchMI[(i,j)] *30
            #miValue =  calculateMI(positionsOfInterest[i],positionsOfInterest[j]) *30
            ellipse(offsetX + i*gridSize +10 ,offsetY + 13 + j*gridSize,miValue,miValue)
            #text("%0.2f" % miValue ,offsetX + i*gridSize,offsetY + j*gridSize) 
            
        
    textFont(largeFont)

def updateLoopPosition():
    global currentLoopPosition
    global loopIncrement
    if(currentLoopPosition>width):
        loopIncrement=-10
    elif(currentLoopPosition<0):
        loopIncrement=10
    currentLoopPosition+=loopIncrement
    
def drawStoredKey():
    text(storedKey,200,300)
    
def drawMapping():
    textSize(30)
    lengthOfLine = width-400
    
    if(mouseIndex == 0):
        myMouseX = mouseX
    elif(mouseIndex==1):
        myMouseX = currentLoopPosition
    
    sliderWidth = map(logoWidth,0,len(mySequences),0,lengthOfLine)
    sliderStart = max(200,myMouseX)
    sliderStart = min(sliderStart,width-200-sliderWidth)
    
    rect(sliderStart,200-5,sliderWidth,10)
    
    global myX
    myX = map(sliderStart,200,width-200-sliderWidth,0,len(mySequences)-logoWidth)

    
    text(str(int(myX))+"_"+str(int(myX+logoWidth))+","+str(logoWidth),width-200,height-30)

    
def drawScale():
    stroke(153)

    fill(color(0))

    textSize(15)
    strokeWeight(10)
    strokeCap(SQUARE)
    line(200,200,width-200,200)
    strokeWeight(1)

    lengthOfLine = width-400
    textAlign(CENTER,BOTTOM)
    for i in range(11):
        ticks = map((lengthOfLine/10)*i,0,lengthOfLine,0,len(mySequences))
        line(200+(lengthOfLine/10)*i,190,200+(lengthOfLine/10)*i,210)
        text(int(ticks),200+(lengthOfLine/10)*i,200)
        
    
    drawMapping()

    
    
def drawLegend():
    textSize(30)

    scale(0.5,1)
    xPosition=130
    for i in range(19):
        text(str(i),xPosition,150)
        xPosition+=130
    scale(2,1)


def drawLogo():
    
    myLogoStats = getTally(mySequences[int(myX):int(myX+logoWidth)])
    
    xPosition = 10
    yPosition = 0
    
    myTextSize = 200
    textSize(myTextSize)
    textAlign(CENTER, TOP)
    
    
    stroke(153)
    line(0,0,width,0)

    
    
    line(0,myTextSize-textDescent(),width,myTextSize-textDescent())
     
    scale(0.5,1)

    for i in range(19):
        xPosition+=130
        for j in range(20):
            if(not myLogoStats[i][j] ==0):
                fill(colorMapping[aaLookup[j]])
                scale(1,myLogoStats[i][j])
                newYPosition = yPosition*(1/myLogoStats[i][j]) -(textDescent()-10)
                text(aaLookup[j],xPosition,newYPosition)
                scale(1,1/myLogoStats[i][j])
                yPosition+=(myLogoStats[i][j]*(myTextSize-textDescent()))
            
        yPosition=0

    fill(color(0))
    scale(2,1)

def getSubset(myInput):
    if("," in myInput):
        pos,letter = myInput.split(",")
        letter=str(letter).upper()
        
        temp = []
        for i in allMySequences:
            if(i[int(pos)]==letter):
                temp.append(i)
                
        if(len(temp)>1):
            return temp
        else:
            return allMySequences
    else:
        return allMySequences

def mousePressed():
    global mouseIndex
    if(mouseIndex==0):
        mouseIndex=1
    else:
        mouseIndex=0
        
def keyPressed():
    
    global logoWidth
    global storedKey
    global mySequences
    global myX
    global colorMapping
    global colorIndex
    global allMySequences
    global mySequences
    global fileIndex
    
    if key == CODED:
        if (keyCode == UP):
            logoWidth= min(logoWidth +1,len(mySequences)-1)
        elif (keyCode == DOWN):
            logoWidth=max(logoWidth -1,1)
        elif (keyCode == LEFT):
            logoWidth=max(logoWidth -100,1)
        elif (keyCode == RIGHT):
            logoWidth=min(logoWidth +100,len(mySequences)-1)

    else:
            
        if (key == ENTER or key == RETURN):
            mySequences = getSubset(storedKey)
            logoWidth=len(mySequences)/10 +1
            myX = 0
            storedKey = ""
        elif (key == TAB):
            if(fileIndex==0):
                allMySequences = open("data/processing_logo_bim.txt",'r').readlines()
                mySequences = allMySequences
                fileIndex=1
            else:
                allMySequences = open("data/processing_logo.txt",'r').readlines()
                mySequences = allMySequences
                fileIndex=0
            logoWidth=len(mySequences)/10 +1
            myX = 0
             
        elif key in 'abcdefghijklmnopqrstuvwxyz1234567890,':
            storedKey=storedKey+key
        elif key == ' ':
            if colorIndex == 1:
                for i in 'RKDENQ':
                    colorMapping[i]=color(0,0,255)
                for i in 'SGHTAP':
                    colorMapping[i]=color(0,255,0)
                for i in 'YVMCLFIW':
                    colorMapping[i]=color(0)
                colorIndex = 0
            elif colorIndex ==0:
                for i in 'GSTYC':
                    colorMapping[i]=color(0,255,0)
                for i in 'QN':
                    colorMapping[i]=color(255,0,255)
                for i in 'KRH':
                    colorMapping[i]=color(0,0,255)
                for i in 'DE':
                    colorMapping[i]=color(255,0,0)
                for i in 'AVLIPWFM':
                    colorMapping[i]=color(0)                
                colorIndex =1
                
            
            
        
    

