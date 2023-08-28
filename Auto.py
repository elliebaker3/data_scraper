import os


districts = os.listdir('newCensus')
for districtT in districts:
    print(districtT)
    if(districtT != 'newCensus'):
        #district = districtT[0]
        info = districtT.split('_')
        print(len(info))
        if len(info) == 3:
            print(info[0])
            print(info[1])
            print(info[2])
            os.system("cp newCensus/{} one.pdf".format(districtT))
            # added this - why didn't I need it before? - deleted code line below - not sure if this is ok to do
            #os.system("mkdir {}".format(info[2]))
            os.system("python CensusAuto.py one.pdf {} {} {}".format(info[0], info[1], info[2]))

