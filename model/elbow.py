FIRST_POINT = 1

def elbowLocator(wcssArr):
    size = len(wcssArr)
    ##arr in size 1 or 2 dealing
    if (size == 1):
        return 1
    if (size == 2):
        if (wcssArr[0]<wcssArr[1]):
            return 1
        else:
            return 2
    
    if (size < 10):
        for i in range (size,10):
            wcssArr.append(wcssArr[size-1])
    size = 10
    #print ('wcssArr: ',wcssArr)
        
    slope = (wcssArr[0]-wcssArr[size-1])/(size-1)
    #print ('slope:',slope)
    max = 0
    index = 0
    for i in range(1, size):
        #print ('grade for',i+1,'clusters:',wcssArr[0]-wcssArr[i]-slope*i)
        if (wcssArr[0]-wcssArr[i]-slope*i)>max:
            max = (wcssArr[0]-wcssArr[i]-slope*i)
            index = i+1
    #print ('number of clusters recomended is:',index)
    return index





    
