# ALMA Data Reduction Script

# Calibration

thesteps = []
step_title = {0: 'Import of the ASDM',
              1: 'Fix of SYSCAL table times',
              2: 'listobs',
              3: 'A priori flagging',
              4: 'Generation and time averaging of the WVR cal table',
              5: 'Generation of the Tsys cal table',
              6: 'Generation of the antenna position cal table',
              7: 'Application of the WVR, Tsys and antpos cal tables',
              8: 'Split out science SPWs and time average',
              9: 'Listobs, and save original flags',
              10: 'Initial flagging *incl. baselines <33m*',
              11: 'Putting a model for the flux calibrator(s)',
              12: 'Save flags before bandpass cal',
              13: 'Bandpass calibration',
              14: 'Save flags before gain cal',
              15: 'Gain calibration',
              16: 'Save flags before applycal',
              17: 'Application of the bandpass and gain cal tables',
              18: 'Split out corrected column',
              19: 'Save flags after applycal'}

if 'applyonly' not in globals(): applyonly = False
try:
  print 'List of steps to be executed ...', mysteps
  thesteps = mysteps
except:
  print 'global variable mysteps not set.'
if (thesteps==[]):
  thesteps = range(0,len(step_title))
  print 'Executing all steps: ', thesteps

# The Python variable 'mysteps' will control which steps
# are executed when you start the script using
#   execfile('scriptForCalibration.py')
# e.g. setting
#   mysteps = [2,3,4]
# before starting the script will make the script execute
# only steps 2, 3, and 4
# Setting mysteps = [] will make it execute all steps.

import re

import os

import casadef

if applyonly != True: es = aU.stuffForScienceDataReduction() 


if re.search('^5.4.0', '.'.join([str(i) for i in cu.version().tolist()[:-1]])) == None:
 sys.exit('ERROR: PLEASE USE THE SAME VERSION OF CASA THAT YOU USED FOR GENERATING THE SCRIPT: 5.4.0')


# CALIBRATE_AMPLI: 
# CALIBRATE_ATMOSPHERE: Callisto,J2000-1748,Venus
# CALIBRATE_BANDPASS: Callisto
# CALIBRATE_DIFFGAIN: 
# CALIBRATE_FLUX: Callisto
# CALIBRATE_FOCUS: 
# CALIBRATE_PHASE: J2000-1748
# CALIBRATE_POINTING: J1743-1658,J2000-1748
# CALIBRATE_POLARIZATION: 
# OBSERVE_CHECK: 
# OBSERVE_TARGET: Venus

# Using reference antenna = DA45,DA54

# Import of the ASDM
mystep = 0
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  if os.path.exists('uid___A002_Xd90607_X10526.ms') == False:
    importasdm('uid___A002_Xd90607_X10526', asis='Antenna Station Receiver Source CalAtmosphere CalWVR CorrelatorMode SBSummary', bdfflags=True, lazy=False, process_caldevice=False)
    if not os.path.exists('uid___A002_Xd90607_X10526.ms.flagversions'):
      print 'ERROR in importasdm. Output MS is probably not useful. Will stop here.'
      thesteps = []
  if applyonly != True: es.fixForCSV2555('uid___A002_Xd90607_X10526.ms')

# Fix of SYSCAL table times
mystep = 1
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  from recipes.almahelpers import fixsyscaltimes
  fixsyscaltimes(vis = 'uid___A002_Xd90607_X10526.ms')

print "# A priori calibration"

# listobs
mystep = 2
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  os.system('rm -rf uid___A002_Xd90607_X10526.ms.listobs')
  listobs(vis = 'uid___A002_Xd90607_X10526.ms',
    listfile = 'uid___A002_Xd90607_X10526.ms.listobs')
  
  

# A priori flagging
mystep = 3
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  flagdata(vis = 'uid___A002_Xd90607_X10526.ms',
    mode = 'manual',
    spw = '5~12,17~32,37~52,57~72',
    autocorr = True,
    flagbackup = False)
  
  flagdata(vis = 'uid___A002_Xd90607_X10526.ms',
    mode = 'manual',
    intent = '*POINTING*,*ATMOSPHERE*',
    flagbackup = False)
  
  flagcmd(vis = 'uid___A002_Xd90607_X10526.ms',
    inpmode = 'table',
    useapplied = True,
    action = 'plot',
    plotfile = 'uid___A002_Xd90607_X10526.ms.flagcmd.png')
  
  flagcmd(vis = 'uid___A002_Xd90607_X10526.ms',
    inpmode = 'table',
    useapplied = True,
    action = 'apply')
  

# Generation and time averaging of the WVR cal table
mystep = 4
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  os.system('rm -rf uid___A002_Xd90607_X10526.ms.wvr') 
  
  os.system('rm -rf uid___A002_Xd90607_X10526.ms.wvrgcal') 
  
  mylogfile = casalog.logfile()
  casalog.setlogfile('uid___A002_Xd90607_X10526.ms.wvrgcal')
  
  wvrgcal(vis = 'uid___A002_Xd90607_X10526.ms',
    caltable = 'uid___A002_Xd90607_X10526.ms.wvr',
    spw = [25, 27, 29, 31, 45, 47, 49, 51, 65, 67, 69, 71],
    smooth = '6.048s',
    toffset = 0,
    tie = ['Venus,J2000-1748'],
    statsource = 'Venus')
  
  casalog.setlogfile(mylogfile)
  
  if applyonly != True: aU.plotWVRSolutions(caltable='uid___A002_Xd90607_X10526.ms.wvr', spw='25', antenna='DA45',
    yrange=[-199,199],subplot=22, interactive=False,
    figfile='uid___A002_Xd90607_X10526.ms.wvr.plots/uid___A002_Xd90607_X10526.ms.wvr') 
  
  #Note: If you see wraps in these plots, try changing yrange or unwrap=True 
  #Note: If all plots look strange, it may be a bad WVR on the reference antenna.
  #      To check, you can set antenna='' to show all baselines.
  

# Generation of the Tsys cal table
mystep = 5
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  os.system('rm -rf uid___A002_Xd90607_X10526.ms.tsys') 
  gencal(vis = 'uid___A002_Xd90607_X10526.ms',
    caltable = 'uid___A002_Xd90607_X10526.ms.tsys',
    caltype = 'tsys')
  
  # Flagging edge channels
  
  flagdata(vis = 'uid___A002_Xd90607_X10526.ms.tsys',
    mode = 'manual',
    spw = '17:0~3;124~127,19:0~3;124~127,21:0~3;124~127,23:0~3;124~127,37:0~3;124~127,39:0~3;124~127,41:0~3;124~127,43:0~3;124~127,57:0~3;124~127,59:0~3;124~127,61:0~3;124~127,63:0~3;124~127',
    flagbackup = False)
  
  if applyonly != True: aU.plotbandpass(caltable='uid___A002_Xd90607_X10526.ms.tsys', overlay='time', 
    xaxis='freq', yaxis='amp', subplot=22, buildpdf=False, interactive=False,
    showatm=True,pwv='auto',chanrange='92.1875%',showfdm=True, showBasebandNumber=True, showimage=False, 
    field='', figfile='uid___A002_Xd90607_X10526.ms.tsys.plots.overlayTime/uid___A002_Xd90607_X10526.ms.tsys') 
  
  
  if applyonly != True: es.checkCalTable('uid___A002_Xd90607_X10526.ms.tsys', msName='uid___A002_Xd90607_X10526.ms', interactive=False) 
  

# Generation of the antenna position cal table
mystep = 6
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  # Warning: no baseline run found for following antenna(s): ['DV20', 'DV18', 'DA65', 'DA64', 'DA63', 'DA48', 'DA60', 'DA45', 'DA44', 'DA47', 'DA46', 'DV15', 'DV14', 'DV17', 'DA42', 'DV23', 'DV24', 'DV21', 'DA62', 'PM01', 'DV08', 'DV09', 'DV11', 'DV10', 'DV22', 'DV04', 'DA52', 'DA53', 'DA50', 'DA51', 'DA56', 'DA57', 'DA54', 'DA55', 'DV06', 'DV07', 'DA58', 'DA59', 'DV02', 'DV03', 'DV16', 'DV13', 'DV05'].
  
  os.system('rm -rf uid___A002_Xd90607_X10526.ms.antpos') 
  gencal(vis = 'uid___A002_Xd90607_X10526.ms',
    caltable = 'uid___A002_Xd90607_X10526.ms.antpos',
    caltype = 'antpos',
    antenna = 'DA42',
  #  parameter = [])
    parameter = [0,0,0])
  
  
  # antenna x_offset y_offset z_offset total_offset baseline_date
  

# Application of the WVR, Tsys and antpos cal tables
mystep = 7
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

# Rescale bad Tsys for Venus
  os.system('rm -r  uid___A002_Xd90607_X10526.ms.Vtsys')
  os.system('cp -r uid___A002_Xd90607_X10526.ms.tsys uid___A002_Xd90607_X10526.ms.Vtsys')
  for s in ['37','39','41','43']:
    aU.replaceTsys('uid___A002_Xd90607_X10526.ms.Vtsys', 'DA47', s, frompol='Y', topol='Y', scaleFactor=0.25)
  
  from recipes.almahelpers import tsysspwmap
  tsysmap = tsysspwmap(vis = 'uid___A002_Xd90607_X10526.ms', tsystable = 'uid___A002_Xd90607_X10526.ms.tsys', tsysChanTol = 1)
   # but seems not to be as good (due to non-standard LO settings) as
  tsysmap=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,21,21,23,23,21,21,23,23,33,34,35,36,37,38,39,40,41,42,43,44,
41,41,43,43,41,41,43,43,53,54,55,56,57,58,59,60,61,62,63,64,61,61,63,63,61,61,63,63]

  # Note: J1743-1658 didn't have any Tsys measurement, and I couldn't find any close measurement. But this is not a science target, so this is probably Ok.
  
  applycal(vis = 'uid___A002_Xd90607_X10526.ms',
    field = '1',
    spw = '25,27,29,31,45,47,49,51,65,67,69,71',
    gaintable = ['uid___A002_Xd90607_X10526.ms.tsys', 'uid___A002_Xd90607_X10526.ms.wvr', 'uid___A002_Xd90607_X10526.ms.antpos'],
    gainfield = ['1', '', ''],
    interp = 'linear,linear',
    spwmap = [tsysmap,[],[]],
    calwt = True,
    flagbackup = False)
  
  
  
  applycal(vis = 'uid___A002_Xd90607_X10526.ms',
    field = '2',
    spw = '25,27,29,31,45,47,49,51,65,67,69,71',
    gaintable = ['uid___A002_Xd90607_X10526.ms.tsys', 'uid___A002_Xd90607_X10526.ms.wvr', 'uid___A002_Xd90607_X10526.ms.antpos'],
    gainfield = ['2', '', ''],
    interp = 'linear,linear',
    spwmap = [tsysmap,[],[]],
    calwt = True,
    flagbackup = False)
  
  
  
  applycal(vis = 'uid___A002_Xd90607_X10526.ms',
    field = '3',
    spw = '25,27,29,31,45,47,49,51,65,67,69,71',
    gaintable = ['uid___A002_Xd90607_X10526.ms.Vtsys', 'uid___A002_Xd90607_X10526.ms.wvr', 'uid___A002_Xd90607_X10526.ms.antpos'],
    gainfield = ['3', '', ''],
    interp = 'linear,linear',
    spwmap = [tsysmap,[],[]],
    calwt = True,
    flagbackup = False)
  
  
  
  if applyonly != True: es.getCalWeightStats('uid___A002_Xd90607_X10526.ms') 
  

# Split out science SPWs and time average
mystep = 8
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  os.system('rm -rf uid___A002_Xd90607_X10526.ms.split') 
  os.system('rm -rf uid___A002_Xd90607_X10526.ms.split.flagversions') 
  
  mstransform(vis = 'uid___A002_Xd90607_X10526.ms',
    outputvis = 'uid___A002_Xd90607_X10526.ms.split',
    datacolumn = 'corrected',
    spw = '25,27,29,31,45,47,49,51,65,67,69,71',
    reindex = False,
    keepflags = True)
  
  

print "# Calibration"

# Listobs, and save original flags
mystep = 9
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  os.system('rm -rf uid___A002_Xd90607_X10526.ms.split.listobs')
  listobs(vis = 'uid___A002_Xd90607_X10526.ms.split',
    listfile = 'uid___A002_Xd90607_X10526.ms.split.listobs')
  
  
  if not os.path.exists('uid___A002_Xd90607_X10526.ms.split.flagversions/Original.flags'):
    flagmanager(vis = 'uid___A002_Xd90607_X10526.ms.split',
      mode = 'save',
      versionname = 'Original')
  
  

# Initial flagging
mystep = 10
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  # Flagging shadowed data
  
  flagdata(vis = 'uid___A002_Xd90607_X10526.ms.split',
    mode = 'shadow',
    flagbackup = False)
 
#end channels 
  flagdata(vis = 'uid___A002_Xd90607_X10526.ms.split',
           spw='29:1875~1919,31:1875~1919,49:1875~1919,51:1875~1919,69:1875~1919,71:1875~1919',
           flagbackup = False)

# short baselines
  flagdata(vis = 'uid___A002_Xd90607_X10526.ms.split',
    mode = 'manual',
    uvrange='0~33m',
    flagbackup = False)

#  flagdata(vis = 'uid___A002_Xd90607_X10526.ms.split',
#    mode = 'manual',
#   antenna='DA57',
#    flagbackup = False)
  
# Putting a model for the flux calibrator(s)
mystep = 11
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  setjy(vis = 'uid___A002_Xd90607_X10526.ms.split',
    field = '1', # Callisto
    spw = '25,27,29,31,45,47,49,51,65,67,69,71',
    standard = 'Butler-JPL-Horizons 2012')
  
  if applyonly != True:
    os.system('rm -rf uid___A002_Xd90607_X10526.ms.split.setjy.field*.png') 
    for i in ['1']:
      plotms(vis = 'uid___A002_Xd90607_X10526.ms.split',
        xaxis = 'uvdist',
        yaxis = 'amp',
        ydatacolumn = 'model',
        field = str(i),
        spw = '25,27,29,31,45,47,49,51,65,67,69,71',
        avgchannel = '9999',
        coloraxis = 'spw',
        plotfile = 'uid___A002_Xd90607_X10526.ms.split.setjy.field'+i+'.png')
  

# Save flags before bandpass cal
mystep = 12
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  
  flagmanager(vis = 'uid___A002_Xd90607_X10526.ms.split',
    mode = 'save',
    versionname = 'BeforeBandpassCalibration')
  
  

# Bandpass calibration
mystep = 13
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  os.system('rm -rf uid___A002_Xd90607_X10526.ms.split.ap_pre_bandpass') 
  
  gaincal(vis = 'uid___A002_Xd90607_X10526.ms.split',
    caltable = 'uid___A002_Xd90607_X10526.ms.split.ap_pre_bandpass',
    field = '1', # Callisto
    spw = '25:0~1919,27:0~1919,29:0~1919,31:0~1919,45:0~1919,47:0~1919,49:0~1919,51:0~1919,65:0~1919,67:0~1919,69:0~1919,71:0~1919',
    scan = '3,5,7',
    solint = 'int',
    refant = 'DA45,DA54',
    uvrange='0~180klambda',
    calmode = 'p')
  
  os.system('rm -rf uid___A002_Xd90607_X10526.ms.split.a_pre_bandpass') 
  
  gaincal(vis = 'uid___A002_Xd90607_X10526.ms.split',
    caltable = 'uid___A002_Xd90607_X10526.ms.split.a_pre_bandpass',
    field = '1', # Callisto
    spw = '25:0~1919,27:0~1919,29:0~1919,31:0~1919,45:0~1919,47:0~1919,49:0~1919,51:0~1919,65:0~1919,67:0~1919,69:0~1919,71:0~1919',
    scan = '3,5,7',
    solint = '60s',
    solnorm=True,
    refant = 'DA45,DA54',
    uvrange='0~180klambda',
    calmode = 'a')
  
  if applyonly != True: es.checkCalTable('uid___A002_Xd90607_X10526.ms.split.ap_pre_bandpass', msName='uid___A002_Xd90607_X10526.ms.split', interactive=False) 
  
  if applyonly != True: es.checkCalTable('uid___A002_Xd90607_X10526.ms.split.a_pre_bandpass', msName='uid___A002_Xd90607_X10526.ms.split', interactive=False) 
  


 # os.system('rm -rf uid___A002_Xd90607_X10526.ms.split.bandpass') 
 # bandpass(vis = 'uid___A002_Xd90607_X10526.ms.split',
 #   caltable = 'uid___A002_Xd90607_X10526.ms.split.bandpass',
 #   field = '1', # Callisto
 #   scan = '3,5,7',
 #   solint = 'inf',
 #   combine = 'scan',
 #   refant = 'DA45,DA54',
 #   uvrange='0~180klambda',
 #   solnorm = True,
 #   bandtype = 'B',
 #   gaintable = ['uid___A002_Xd90607_X10526.ms.split.ap_pre_bandpass','uid___A002_Xd90607_X10526.ms.split.a_pre_bandpass'])
  
  os.system('rm -rf uid___A002_Xd90607_X10526.ms.split.bandpass_smooth20ch') 
  
  bandpass(vis = 'uid___A002_Xd90607_X10526.ms.split',
    caltable = 'uid___A002_Xd90607_X10526.ms.split.bandpass_smooth20ch',
    field = '1', # Callisto
    scan = '3,5,7',
    solint = 'inf,8MHz',
    combine = 'scan',
    refant = 'DA45,DA54',
    uvrange='0~180klambda',
    minblperant=2,
    minsnr=1,
    solnorm = True,
    bandtype = 'B',
    gaintable = ['uid___A002_Xd90607_X10526.ms.split.ap_pre_bandpass','uid___A002_Xd90607_X10526.ms.split.a_pre_bandpass'])

  
  if applyonly != True: es.checkCalTable('uid___A002_Xd90607_X10526.ms.split.bandpass_smooth20ch', msName='uid___A002_Xd90607_X10526.ms.split', interactive=False) 
  
#  if applyonly != True: es.checkCalTable('uid___A002_Xd90607_X10526.ms.split.bandpass', #msName='uid___A002_Xd90607_X10526.ms.split', interactive=False) 
  

# Save flags before gain cal
mystep = 14
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  
  flagmanager(vis = 'uid___A002_Xd90607_X10526.ms.split',
    mode = 'save',
    versionname = 'BeforeGainCalibration')
  
  

# Gain calibration
mystep = 15
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  # Note: the Solar system object used for flux calibration is highly resolved on some baselines.
  # Note: we will first determine the flux of the phase calibrator(s) on a subset of antennas.
  
  delmod('uid___A002_Xd90607_X10526.ms.split',field='2')
  
  os.system('rm -rf uid___A002_Xd90607_X10526.ms.split.phase_short_int') 
  gaincal(vis = 'uid___A002_Xd90607_X10526.ms.split',
    caltable = 'uid___A002_Xd90607_X10526.ms.split.phase_short_int',
    field = '1', # Callisto
    selectdata = True,
    spw='25,27,29:0~1290;1320~1919,31,45,47,49:0~1290;1320~1919,51,65,67,69:0~1290;1320~1919,71',
    uvrange='0~180klambda',
#    antenna = 'DA42,DA44,DA45,DA54,DA46,DA47,DA48,DA50,DA51,DA52,DA53,DA54,DA55,DA56,DA57,DA58,DA59,DA60,DA62,DA63,DA64,DV02,DV03,DV04,DV05,DV06,DV07,DV08,DV11,DV13,DV14,DV15,DV18,DV21,DV22,DV23,DV24&',
    solint = 'int',
    refant = 'DA45,DA54',
    gaintype = 'G',
    calmode = 'p',
    gaintable = 'uid___A002_Xd90607_X10526.ms.split.bandpass_smooth20ch')
  
  gaincal(vis = 'uid___A002_Xd90607_X10526.ms.split',
    caltable = 'uid___A002_Xd90607_X10526.ms.split.phase_short_int',
    field = '2', # J2000-1748
    selectdata = True,
    spw='25,27,29:0~1290;1320~1919,31,45,47,49:0~1290;1320~1919,51,65,67,69:0~1290;1320~1919,71',
    solint = 'int',
    refant = 'DA45,DA54',
    gaintype = 'G',
    calmode = 'p',
    append = True,
    gaintable = 'uid___A002_Xd90607_X10526.ms.split.bandpass_smooth20ch')
  
  if applyonly != True: es.checkCalTable('uid___A002_Xd90607_X10526.ms.split.phase_short_int', msName='uid___A002_Xd90607_X10526.ms.split', interactive=False) 
  
  os.system('rm -rf uid___A002_Xd90607_X10526.ms.split.ampli_short_inf') 
  gaincal(vis = 'uid___A002_Xd90607_X10526.ms.split',
    caltable = 'uid___A002_Xd90607_X10526.ms.split.ampli_short_inf',
    field = '1,2', # Callisto,J2000-1748
    selectdata = True,
    spw='25,27,29:0~1290;1320~1919,31,45,47,49:0~1290;1320~1919,51,65,67,69:0~1290;1320~1919,71',
    solint = 'inf',
    refant = 'DA45,DA54',
    gaintype = 'T',
    calmode = 'a',
    gaintable = ['uid___A002_Xd90607_X10526.ms.split.bandpass_smooth20ch', 'uid___A002_Xd90607_X10526.ms.split.phase_short_int'])
  
  if applyonly != True: es.checkCalTable('uid___A002_Xd90607_X10526.ms.split.ampli_short_inf', msName='uid___A002_Xd90607_X10526.ms.split', interactive=False) 
  
  os.system('rm -rf uid___A002_Xd90607_X10526.ms.split.flux_short_inf') 
  os.system('rm -rf uid___A002_Xd90607_X10526.ms.split.fluxscale') 
  mylogfile = casalog.logfile()
  casalog.setlogfile('uid___A002_Xd90607_X10526.ms.split.fluxscale')
  
  fluxscaleDict = fluxscale(vis = 'uid___A002_Xd90607_X10526.ms.split',
    caltable = 'uid___A002_Xd90607_X10526.ms.split.ampli_short_inf',
    fluxtable = 'uid___A002_Xd90607_X10526.ms.split.flux_short_inf',
    reference = '1') # Callisto
  
  casalog.setlogfile(mylogfile)
  
  if applyonly != True: es.fluxscale2(caltable = 'uid___A002_Xd90607_X10526.ms.split.ampli_short_inf', removeOutliers=True, msName='uid___A002_Xd90607_X10526.ms', writeToFile=True, preavg=10000)
  
  f = open('uid___A002_Xd90607_X10526.ms.split.fluxscale')
  fc = f.readlines()
  f.close()
  
  for phaseCalName in ['J2000-1748']:
    for i in range(len(fc)):
      if fc[i].find('Flux density for '+phaseCalName) != -1 and re.search('in SpW=[0-9]+(?: \(.*?\))? is: [0-9]+\.[0-9]+', fc[i], re.DOTALL|re.IGNORECASE) is not None:
        line = (re.search('in SpW=[0-9]+(?: \(.*?\))? is: [0-9]+\.[0-9]+', fc[i], re.DOTALL|re.IGNORECASE)).group(0)
        spwId = (line.split('='))[1].split()[0]
        flux = float((line.split(':'))[1].split()[0])
        setjy(vis = 'uid___A002_Xd90607_X10526.ms.split',
          field = phaseCalName.replace(';','*;').split(';')[0],
          spw = spwId,
          standard = 'manual',
          fluxdensity = [flux,0,0,0])
  
  os.system('rm -rf uid___A002_Xd90607_X10526.ms.split.phase_int') 
  gaincal(vis = 'uid___A002_Xd90607_X10526.ms.split',
    caltable = 'uid___A002_Xd90607_X10526.ms.split.phase_int',
    field = '2', # J2000-1748
    spw='25,27,29:0~1290;1320~1919,31,45,47,49:0~1290;1320~1919,51,65,67,69:0~1290;1320~1919,71',
    solint = 'int',
    refant = 'DA45,DA54',
    gaintype = 'G',
    calmode = 'p',
    gaintable = 'uid___A002_Xd90607_X10526.ms.split.bandpass_smooth20ch')
  
  if applyonly != True: es.checkCalTable('uid___A002_Xd90607_X10526.ms.split.phase_int', msName='uid___A002_Xd90607_X10526.ms.split', interactive=False) 
  
#  os.system('rm -rf uid___A002_Xd90607_X10526.ms.split.Cphase_int') 
#  gaincal(vis = 'uid___A002_Xd90607_X10526.ms.split',
#    caltable = 'uid___A002_Xd90607_X10526.ms.split.Cphase_int',
#    field = '1', # Callisto
#    spw='25,27,29:0~1290;1320~1919,31,45,47,49:0~1290;1320~1919,51,65,67,69:0~1290;1320~1919,71',
#    solint = 'int',
#    uvrange='0~180klambda',
#    refant = 'DA45,DA54',
#    gaintype = 'G',
#    calmode = 'p',
#    gaintable = 'uid___A002_Xd90607_X10526.ms.split.bandpass_smooth20ch')
#  
#  if applyonly != True: es.checkCalTable('uid___A002_Xd90607_X10526.ms.split.Cphase_int', msName='uid___A002_Xd90607_X10526.ms.split', interactive=False) 
 
  os.system('rm -rf uid___A002_Xd90607_X10526.ms.split.flux_inf') 
  gaincal(vis = 'uid___A002_Xd90607_X10526.ms.split',
    caltable = 'uid___A002_Xd90607_X10526.ms.split.flux_inf',
    field = '2', # J2000-1748
    spw='25,27,29:0~1290;1320~1919,31,45,47,49:0~1290;1320~1919,51,65,67,69:0~1290;1320~1919,71',
    solint = 'inf',
    refant = 'DA45,DA54',
    gaintype = 'T',
    calmode = 'a',
    gaintable = ['uid___A002_Xd90607_X10526.ms.split.bandpass_smooth20ch', 'uid___A002_Xd90607_X10526.ms.split.phase_int'])

  if applyonly != True: es.checkCalTable('uid___A002_Xd90607_X10526.ms.split.flux_inf', msName='uid___A002_Xd90607_X10526.ms.split', interactive=False) 

 
#  os.system('rm -rf uid___A002_Xd90607_X10526.ms.split.Cflux_30s') 
#  gaincal(vis = 'uid___A002_Xd90607_X10526.ms.split',
#    caltable = 'uid___A002_Xd90607_X10526.ms.split.Cflux_30s',
#    field = '1', # Callisto
#    spw='25,27,29:0~1290;1320~1919,31,45,47,49:0~1290;1320~1919,51,65,67,69:0~1290;1320~1919,71',
#    solint = '30s',
#    refant = 'DA45,DA54',
#    uvrange='0~180klambda',
#    gaintype = 'T',
#    calmode = 'a',
#    gaintable = ['uid___A002_Xd90607_X10526.ms.split.bandpass_smooth20ch', 'uid___A002_Xd90607_X10526.ms.split.Cphase_int'])
#  
#  if applyonly != True: es.checkCalTable('uid___A002_Xd90607_X10526.ms.split.Cflux_30s', msName='uid___A002_Xd90607_X10526.ms.split', interactive=False) 
  
  os.system('rm -rf uid___A002_Xd90607_X10526.ms.split.phase_inf') 
  gaincal(vis = 'uid___A002_Xd90607_X10526.ms.split',
    caltable = 'uid___A002_Xd90607_X10526.ms.split.phase_inf',
    field = '2', # J2000-1748
    spw='25,27,29:0~1290;1320~1919,31,45,47,49:0~1290;1320~1919,51,65,67,69:0~1290;1320~1919,71',
    solint = 'inf',
    refant = 'DA45,DA54',
    gaintype = 'G',
    calmode = 'p',
    gaintable = 'uid___A002_Xd90607_X10526.ms.split.bandpass_smooth20ch')
  
  if applyonly != True: es.checkCalTable('uid___A002_Xd90607_X10526.ms.split.phase_inf', msName='uid___A002_Xd90607_X10526.ms.split', interactive=False) 
  

# Save flags before applycal
mystep = 16
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  
  flagmanager(vis = 'uid___A002_Xd90607_X10526.ms.split',
    mode = 'save',
    versionname = 'BeforeApplycal')
  
  

# Application of the bandpass and gain cal tables
mystep = 17
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

#  for i in ['1']: # Callisto
#    applycal(vis = 'uid___A002_Xd90607_X10526.ms.split',
#      field = str(i),
#      gaintable = ['uid___A002_Xd90607_X10526.ms.split.bandpass_smooth20ch', 'uid___A002_Xd90607_X10526.ms.split.Cphase_int', 'uid___A002_Xd90607_X10526.ms.split.Cflux_30s'],
#      gainfield = ['', i, i],
#      interp = 'linear,linear',
#      calwt = True,
#      flagbackup = False)


#  applycal(vis = 'uid___A002_Xd90607_X10526.ms.split',
#    field = '2', # J2000
#    gaintable = ['uid___A002_Xd90607_X10526.ms.split.bandpass_smooth20ch', 'uid___A002_Xd90607_X10526.ms.split.phase_int', 'uid___A002_Xd90607_X10526.ms.split.flux_inf'],
#    gainfield = ['', '2', '2'], # J2000-1748
#    interp = 'linear,linear',
#    calwt = True,
#    flagbackup = False)  

  applycal(vis = 'uid___A002_Xd90607_X10526.ms.split',
    field = '3', # Venus
#    gaintable = ['uid___A002_Xd90607_X10526.ms.split.bandpass_smooth20ch', 'uid___A002_Xd90607_X10526.ms.split.phase_inf', 'uid___A002_Xd90607_X10526.ms.split.flux_inf'],
    gaintable = ['uid___A002_Xd90607_X10526.ms.split.phase_inf', 'uid___A002_Xd90607_X10526.ms.split.flux_inf'],
    gainfield = ['', '2', '2'], # J2000-1748
    interp = 'linear,linear',
    calwt = True,
    flagbackup = False)
  

# Split out corrected column
mystep = 18
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  os.system('rm -rf uid___A002_Xd90607_X10526.ms.split.cal') 
  os.system('rm -rf uid___A002_Xd90607_X10526.ms.split.cal.flagversions') 
  
  listOfIntents = ['CALIBRATE_BANDPASS#ON_SOURCE',
   'CALIBRATE_FLUX#ON_SOURCE',
   'CALIBRATE_PHASE#ON_SOURCE',
   'CALIBRATE_WVR#AMBIENT',
   'CALIBRATE_WVR#HOT',
   'CALIBRATE_WVR#OFF_SOURCE',
   'CALIBRATE_WVR#ON_SOURCE',
   'OBSERVE_TARGET#ON_SOURCE']
  
  os.system('rm -rf uid___A002_Xd90607_X10526.ms.split.cal')
  mstransform(vis = 'uid___A002_Xd90607_X10526.ms.split',
    outputvis = 'uid___A002_Xd90607_X10526.ms.split.cal',
    datacolumn = 'corrected',
    intent = ','.join(listOfIntents),
    keepflags = True)
  
  

# Save flags after applycal
mystep = 19
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  
  flagmanager(vis = 'uid___A002_Xd90607_X10526.ms.split.cal',
    mode = 'save',
    versionname = 'AfterApplycal')
  
  
