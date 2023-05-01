import pandas as pd
def change_values(oldList, values):
    newList = []
    for obj in oldList:
        for i in range(0, len(values)):
            if (obj==i+1):
                newList.append(values[i])
                break
        if (obj != (i+1)):
            print (f'#### VALUE ERROR {obj} is not {i+1} #######')
            newList.append('?')
    #print ('newList (', len(newList), '): ', newList)
    return newList

if __name__ == '__main__':
    df = pd.read_csv('datasets/lympo/lymphography.csv')
    print ('headers: ', df.columns.values)
    newdf = pd.DataFrame()
    i=0
    
    print (df.columns.values[i],'(',len(df[df.columns.values[i]]),'): ', list(df[df.columns.values[i]]))
    newdf['lymphatics']=change_values(df['lymphatics'],['normal','arched','deformed','displaced'])
    i = i+1
    
    print (df.columns.values[i],'(',len(df[df.columns.values[i]]),'): ', list(df[df.columns.values[i]]))
    newdf['block of affere']=change_values(df['block of affere'],['no','yes'])
    i = i+1

    print (df.columns.values[i],'(',len(df[df.columns.values[i]]),'): ', list(df[df.columns.values[i]]))
    newdf['bl. of lymph. c']=change_values(df['bl. of lymph. c'],['no','yes'])
    i = i+1

    print (df.columns.values[i],'(',len(df[df.columns.values[i]]),'): ', list(df[df.columns.values[i]]))
    newdf['bl. of lymph. s']=change_values(df['bl. of lymph. s'],['no','yes'])
    i = i+1
    
    print (df.columns.values[i],'(',len(df[df.columns.values[i]]),'): ', list(df[df.columns.values[i]]))
    newdf['by pass']=change_values(df['by pass'],['no','yes'])
    i = i+1
    
    print (df.columns.values[i],'(',len(df[df.columns.values[i]]),'): ', list(df[df.columns.values[i]]))
    newdf['extravasates']=change_values(df['extravasates'],['no','yes'])
    i = i+1

    print (df.columns.values[i],'(',len(df[df.columns.values[i]]),'): ', list(df[df.columns.values[i]]))
    newdf['regeneration of']=change_values(df['regeneration of'],['no','yes'])
    i = i+1

    print (df.columns.values[i],'(',len(df[df.columns.values[i]]),'): ', list(df[df.columns.values[i]]))
    newdf['early uptake in']=change_values(df['early uptake in'],['no','yes'])
    i = i+1

    print (df.columns.values[i],'(',len(df[df.columns.values[i]]),') COPY: ', list(df[df.columns.values[i]]))
    newdf['lym.nodes dimin']=df['lym.nodes dimin']
    i = i+1
    
    print (df.columns.values[i],'(',len(df[df.columns.values[i]]),') COPY: ', list(df[df.columns.values[i]]))
    newdf['lym.nodes enlar']=df['lym.nodes enlar']
    i = i+1

    print (df.columns.values[i],'(',len(df[df.columns.values[i]]),'): ', list(df[df.columns.values[i]]))
    newdf['changes in lym']=change_values(df['changes in lym'],['bean','oval','round'])
    i = i+1

    print (df.columns.values[i],'(',len(df[df.columns.values[i]]),'): ', list(df[df.columns.values[i]]))
    newdf['defect in node']=change_values(df['defect in node'],['no','lacunar','lac. marginal','lac. central'])
    i = i+1

    print (df.columns.values[i],'(',len(df[df.columns.values[i]]),'): ', list(df[df.columns.values[i]]))
    newdf['changes in node']=change_values(df['changes in node'],['no','lacunar','lac. marginal','lac. central'])
    i = i+1

    print (df.columns.values[i],'(',len(df[df.columns.values[i]]),'): ', list(df[df.columns.values[i]]))
    newdf['changes in stru']=change_values(df['changes in stru'],['no','grainy','drop-like','coarse','diluted','reticular','stripped','faint'])
    i = i+1

    print (df.columns.values[i],'(',len(df[df.columns.values[i]]),'): ', list(df[df.columns.values[i]]))
    newdf['special forms']=change_values(df['special forms'],['no','chalices','vesicles'])
    i = i+1

    print (df.columns.values[i],'(',len(df[df.columns.values[i]]),'): ', list(df[df.columns.values[i]]))
    newdf['dislocation of']=change_values(df['dislocation of'],['no','yes'])
    i = i+1
    
    print (df.columns.values[i],'(',len(df[df.columns.values[i]]),'): ', list(df[df.columns.values[i]]))
    newdf['exclusion of no']=change_values(df['exclusion of no'],['no','yes'])
    i = i+1
    
    print (df.columns.values[i],'(',len(df[df.columns.values[i]]),'): ', list(df[df.columns.values[i]]))
    newdf['no. of nodes in']=change_values(df['no. of nodes in'],['0-9','10-19','20-29','30-39','40-49','50-59','60-69','>=70'])
    i = i+1

    print (df.columns.values[i],'(',len(df[df.columns.values[i]]),'): ', list(df[df.columns.values[i]]))
    newdf['class']=change_values(df['class'],['normal find','metastases','malign lymph','fibrosis'])
    
    newdf.to_csv('datasets/lympo/categoryLympo.csv', index=False)
















