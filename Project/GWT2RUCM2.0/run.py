from response.rucmresponse import RUCMGnerator 
from support.nlpsupport import NLPExecutor
from response.gwtresponse import GWTImporter
from response.backgroundresponse import BackgroundImporter
import sys
if __name__ == '__main__':
    nlp = NLPExecutor()
    importer = GWTImporter(nlp)
    bgimporter = BackgroundImporter(nlp)
    generator = RUCMGnerator(nlp)
    seg=None
    pos=None
    gwtfile=None
    for i in range(1,len(sys.argv)):
        if i == '-s':
            seg = sys.argv[i+1]
            continue
        if sys.argv[i] == '-p':
            pos = sys.argv[i+1]
            continue
        if sys.argv[i] == '-i':
            gwtfile = sys.argv[i+1]
            continue
    bgimporter.importBackground(seg,pos) 
    gwtlist = importer.importGWT(filepath=gwtfile)
    generator.generateRUCMs(gwtlist)