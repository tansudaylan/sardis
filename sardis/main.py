import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np

import datetime, os

import troia
import tdpy
import nicomedia


def retr_pathsard(pathbase=None, strgcnfg=None):
    """Return normalized Sardis base and output paths."""

    pathbasesard = tdpy.retr_pathbase('sardis')
    if pathbase is None:
        pathbase = pathbasesard
    else:
        pathbase = tdpy.ensr_path(pathbase)

    pathdatapipe = tdpy.ensr_path(os.path.join(pathbase, 'data'))
    pathvisupipe = tdpy.ensr_path(os.path.join(pathbase, 'visuals'))

    dictpath = {
        'pathbasesard': pathbasesard,
        'pathbase': pathbase,
        'pathdatapipe': pathdatapipe,
        'pathvisupipe': pathvisupipe,
    }
    if strgcnfg is not None:
        pathcnfg = tdpy.ensr_path(os.path.join(pathbase, strgcnfg))
        dictpath['pathcnfg'] = pathcnfg
        dictpath['pathsimu'] = tdpy.ensr_path(os.path.join(pathcnfg, 'simulation'))
        dictpath['pathobsd'] = tdpy.ensr_path(os.path.join(pathcnfg, 'observed'))

    return dictpath

def init(
         
         typesyst='PlanetarySystem', \

         dicttroiinpt=None, \
         
         # a string distinguishing the run to be used in the file names
         strgcnfg=None, \
         
         # the path in which the run folder will be placed
         pathbase=None, \
        
        ):
    '''
    Run troia on simulated and observed data, inferring the occurrence rate
    '''
    
    # construct global object
    gdat = tdpy.gdatstrt()
    
    # copy locals (inputs) to the global object
    for attr, valu in locals().items():
        if '__' not in attr and attr != 'gdat':
            setattr(gdat, attr, valu)

    # string for date and time
    gdat.strgtimestmp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
   
    print('sardis initialized at %s...' % gdat.strgtimestmp)
    
    # paths
    ## path of the sardis data folder
    if gdat.strgcnfg is None:
        gdat.strgcnfg = '%s' % (gdat.typesyst)

    dictpath = retr_pathsard(pathbase=gdat.pathbase, strgcnfg=gdat.strgcnfg)
    for attr, valu in dictpath.items():
        setattr(gdat, attr, valu)

    #listtoiitarg = np.loadtxt(path)

    dictmileinptglob = dict()
    #dictmileinptglob['dictboxsperiinpt'] = dict()
    #dictmileinptglob['dictboxsperiinpt']['factosam'] = 0.1
    
    gdat.typepoplsimu = 'Synthetic'

    # select targets
    if gdat.typepoplsimu == 'TIC_m060':
        dictpopltici = nicomedia.retr_dictpopltic8(typepopl='TIC_m060')
        listtici = dictpopltici['TIC']
    
    if gdat.dicttroiinpt is None:
        gdat.dicttroiinpt = dict()
        gdat.dicttroiinpt['pathbase'] = gdat.pathsimu
        gdat.dicttroiinpt['typesyst'] = gdat.typesyst
        gdat.dicttroiinpt['listlablinst'] = [['TESS'], []]
        if gdat.typepoplsimu == 'Synthetic':
            gdat.dicttroiinpt['liststrgtypedata'] = [['simutargsynt'], []]
        else:
            gdat.dicttroiinpt['liststrgtypedata'] = [['simutargpartinje'], []]

    # simulated run to get the precision and recall
    dicttroyoutp = troia.init( \
               **gdat.dicttroiinpt, \
               #listtoiitarg=listtoiitarg, \
               #listlablinst=[['TESS'], []], \
               #typepopl='prev', \
              )

    troia.init()

