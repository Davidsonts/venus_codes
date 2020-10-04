"""
Script to self-calibrate the Venus data for project 2018.A.00023.S, after running 
uid___A002_Xd90607_X10526.ms.scriptForCalibration33.py
uid___A002_Xd90607_X10f75.ms.scriptForCalibration33.py
on the observed ASDM.  The starting point is the files with
instrumental, bandpass and phase calibration applied, *split.cal

Each command is selected manually as required.

"""
##############################

# Calibrated visibility data
vissV=['../analysis/X10526/uid___A002_Xd90607_X10526.ms.split.cal','../analysis/X10f75/uid___A002_Xd90607_X10f75.ms.split.cal']

# Science spectral windows. 
spws= ['25', '27', '29', '31', '45', '47', '49', '51', '65', '67', '69', '71']

# Names for output files
thevis = ['Venus254565.ms','Venus274767.ms','Venus294969.ms','Venus315171.ms']

# 
xWvis=['Venus294969.ms','Venus315171.ms']
xNvis=['Venus254565.ms','Venus274767.ms']

# spw centred close to 266.9 GHz, adjusted for the Venus ephemeris
# Visibility data channel width 61.035 kHz
lspws=['25', '45', '65']   
# Visibilitydata channel width 976.562 kHz
cspws=['29', '49', '69']

##########
# Process narrow-band data

# Split out the appropriate Venus spw, preserving the ephemeris
for i in range(len(lspws)):
#    for v in vissV:
      os.system('rm -rf Venus'+v[38:44]+'spw'+lspws[i]+'.ms')
      mstransform(vis=v,
                outputvis='Venus'+v[38:44]+'spw'+lspws[i]+'.ms',
                field='Venus',
                spw=lspws[i],
                datacolumn='data',
                regridms=True,
                phasecenter='VENUS',
                outframe='')

# Concatenate into a single file
Venus=[]
for i in range(3):
      for v in vissV:
        Venus.append('Venus'+v[38:44]+'spw'+lspws[i]+'.ms')

os.system('rm -rf Venus254565.ms')
concat(vis=Venus,
           concatvis='Venus254565.ms',
           forcesingleephemfield='Venus',
           freqtol='100MHz')

flagmanager(vis='Venus254565.ms',
            mode='save',
            versionname='original')

# Inspect data and flag some noisy data
flagdata(vis='Venus254565.ms',
         mode='manual',
         scan='28,30',
         antenna='DA60&DV09')

flagdata(vis='Venus254565.ms',
         mode='manual',
         scan='12,14,20,22,28,30',
         antenna='DA53&DA56')

# Insert model for Venus
setjy(vis='Venus254565.ms',
      field='Venus',
      standard='Butler-JPL-Horizons 2012',
      usescratch=True)


############################
# Self-calibrate - phase-only, excluding the central channels
os.system('rm -rf Venus254565.ms.p30s')
gaincal(vis='Venus254565.ms',
          caltable='Venus254565.ms.p130s',
          solint='30s',
          spw='0:0~720;1119~1919',
          minsnr=3,
          refant='DA45',
          calmode='p')

flagmanager(vis='Venus254565.ms',
              mode='save',
              versionname='preapplycal')

# Apply calibration
applycal(vis='Venus254565.ms',
           calwt=False,
           gaintable='Venus254565.ms.p130s')           


# Select channels clear of expected line
contchanslsub='0:0~760;1159~1919'  

# Subtract first-order continuum
os.system('rm -rf Venus254565.ms.contsub')
uvcontsub(vis='Venus254565.ms',
                fitspw=contchanslsub,
                combine='scan',
                fitorder=1)



#######################################################################
# Process wide-band data

# Split out the appropriate Venus spw, preserving the ephemeris
for i in range(len(cspws)):
#    for v in vissV:
      os.system('rm -rf Venus'+v[38:44]+'spw'+cspws[i]+'.ms')
      mstransform(vis=v,
                outputvis='Venus'+v[38:44]+'spw'+cspws[i]+'.ms',
                field='Venus',
                spw=cspws[i],
                datacolumn='data',
                regridms=True,
                phasecenter='VENUS',
                outframe='')

# Concatenate into a single file
Venus=[]
for i in range(3):
      for v in vissV:
        Venus.append('Venus'+v[38:44]+'spw'+cspws[i]+'.ms')

os.system('rm -rf Venus294969.ms')
concat(vis=Venus,
           concatvis='Venus294969.ms',
           forcesingleephemfield='Venus',
           freqtol='100MHz')

flagmanager(vis='Venus294969.ms',
            mode='save',
            versionname='original')

# Inspect data and flag some noisy data
flagdata(vis='Venus294969.ms',
         mode='manual',
         scan='28,30',
         antenna='DA60&DV09')

flagdata(vis='Venus294969.ms',
         mode='manual',
         scan='12,14,20,22,28,30',
         antenna='DA53&DA56')

# Insert model for Venus
setjy(vis='Venus294969.ms',
      field='Venus',
      standard='Butler-JPL-Horizons 2012',
      usescratch=True)


############################
# Self-calibrate - phase-only, excluding the central channels
os.system('rm -rf Venus294969.ms.p30s')
gaincal(vis='Venus294969.ms',
          caltable='Venus294969.ms.p130s',
          solint='30s',
          spw='0:0~720;1119~1919',
          minsnr=3,
          refant='DA45',
          calmode='p')

flagmanager(vis='Venus294969.ms',
              mode='save',
              versionname='preapplycal')

# Apply calibration
applycal(vis='Venus294969.ms',
           calwt=False,
           gaintable='Venus294969.ms.p130s')           

################
# Make image cube including continuum
os.system('rm -rf Venus294969_cube_p130s-33.clean_nosub*')
tclean(vis = 'Venus294969.ms',
         imagename = 'Venus294969_cube_p130s-33.clean_nosub',
         field = 'Venus',
         datacolumn='corrected',
         phasecenter = 'TRACKFIELD',
         stokes = 'I',
         specmode = 'cubesource',
         restfreq='266.944662GHz',
         width='5km/s',
         imsize = [200, 200],
         cell = '0.16arcsec',
         deconvolver = 'multiscale',
         scales=[0,5,10,15], 
         cyclefactor=2.0,   # trying to avoid basket weaving
         minpsffraction=0.2,#   by more frequent major cycles
         niter = 1500000,    # 
         cycleniter = 20000,
         mask = 'circle[[121pix, 96pix],50pix]',
         threshold='0.002Jy', #
         restoringbeam='common',
         weighting = 'briggs',
         robust = 0.5,
         gridder = 'standard',
         pbcor = True,
         interactive = True
         )

################

# The broad band contains a telluric line; pick continuum-only
# channels to avoid this and the potential Venus line
# Perform a 1st-order continuum subtraction

contchanslsub2='0:0~650;1100~1199'

os.system('rm -rf Venus294969.ms.contsub2')
uvcontsub(vis='Venus294969.ms',
                fitspw=contchanslsub2,
                combine='scan',
                fitorder=1)
os.system('mv Venus294969.ms.contsub Venus294969.ms.contsub2')

# Image the broad-band continuum-subtracted cube
os.system('rm -rf Venus294969_cube_p130s-33.clean_fit2*')
tclean(vis = 'Venus294969.ms.contsub2',
         imagename = 'Venus294969_cube_p130s-33.clean_fit2',
         field = 'Venus',
         datacolumn='corrected',
         phasecenter = 'TRACKFIELD',
         stokes = 'I',
         specmode = 'cubesource',
         restfreq='266.944662GHz',
         start='-300 km/s',
         nchan=120,
         width='5km/s',
         imsize = [200, 200],
         cell = '0.16arcsec',
         deconvolver = 'multiscale',
         scales=[0,5,10,15], 
         cyclefactor=2.0,   # trying to avoid basket weaving
         minpsffraction=0.2,#   by more frequent major cycles
         niter = 100000,    # try 50000 for single broad spw
         cycleniter = 20000,
         mask = 'circle[[121pix, 96pix],50pix]',
         threshold='0.003Jy', #
         restoringbeam='common',
         weighting = 'briggs',
         robust = 0.5,
         gridder = 'standard',
         pbcor = True,
         interactive = True
         )


###########  LINE
# split out Venus for line spw only
for i in range(len(lspws)):
    for v in vissV:
      os.system('rm -rf Venus'+v[38:44]+'spw'+lspws[i]+'.ms')
      mstransform(vis=v,
                outputvis='Venus'+v[38:44]+'spw'+lspws[i]+'.ms',
                field='Venus',
                spw=lspws[i],
                datacolumn='data',
                regridms=True,
                phasecenter='VENUS',
                outframe='')

Venus=[]
for i in range(3):
      for v in vissV:
        Venus.append('Venus'+v[38:44]+'spw'+lspws[i]+'.ms')


# Work onjust one tuning
os.system('rm -rf Venus254565.ms')
concat(vis=Venus,
           concatvis='Venus254565.ms',
           forcesingleephemfield='Venus',
           freqtol='10MHz')

flagmanager(vis='Venus254565.ms',
            mode='save',
            versionname='original')

############################
# Selfcal

setjy(vis='Venus254565.ms',
      field='Venus',
      standard='Butler-JPL-Horizons 2012',
      usescratch=True)

flagdata(vis='Venus254565.ms',
         mode='manual',
         scan='28,30',
         antenna='DA60&DV09')

#flagdata(vis='Venus254565.ms',
#         mode='list',
#         inpfile='flags.log',
#         flagbackup=False)

        
os.system('rm -rf Venus254565.ms.p30s')
gaincal(vis='Venus254565.ms',
          caltable='Venus254565.ms.p130s',
          solint='30s',
          spw='0:0~720;1119~1919',
          minsnr=3,
          refant='DA45',
          calmode='p')

#flagmanager

flagmanager(vis='Venus254565.ms',
              mode='save',
              versionname='preapplycal')

applycal(vis='Venus254565.ms',
           calwt=False,
           gaintable='Venus254565.ms.p130s')           

contchanslsub='0:0~760;1159~1919'  # 
# centre excluded from blcal approx 95~145 for all channels avg to .55 km/s
# but NB imaging excludes end channels, non-bl-cal range -2~25 km/s 

uvcontsub(vis='Venus254565.ms',
                fitspw=contchanslsub,
                combine='scan',
                fitorder=1)

# Make cube at 0.55 km/s resolution
tclean(vis = 'Venus254565.ms',
         imagename = 'Venus254565_p30s_cont.clean',
         field = 'Venus',
         datacolumn='corrected',
         phasecenter = 'TRACKFIELD',
         stokes = 'I',
         specmode = 'mfs',
         spw='0:645~744',
         imsize = [200, 200],
         cell = '0.16arcsec',
         deconvolver = 'multiscale',
         scales=[0,5,10,15], 
         cyclefactor=2.0,   # trying to avoid basket weaving
         minpsffraction=0.2,#   by more frequent major cycles
         niter = 100000,    # try 50000 for single broad spw
         cycleniter = 100000,
         threshold='0.005Jy',
         weighting = 'briggs',
         robust = 0.5,
         mask = '',
         gridder = 'standard',
         pbcor = True,
         interactive = True
         )

# fullres
# Vel 0 in chan 328 = orig chan 958
os.system('rm -rf Venus254565_cube_p130s-33.clean_fullres*')
tclean(vis = 'Venus254565.ms.contsub',
         imagename = 'Venus254565_cube_p130s-33.clean_fullres',
         field = 'Venus',
         datacolumn='corrected',
         phasecenter = 'TRACKFIELD',
         stokes = 'I',
         specmode = 'cubesource',
         restfreq='266.944662GHz',
         start=630,
         nchan=642,
         width='0.55km/s',
         imsize = [200, 200],
         cell = '0.16arcsec',
         deconvolver = 'multiscale',
         scales=[0,5,10,15], 
         cyclefactor=2.0,   # trying to avoid basket weaving
         minpsffraction=0.2,#   by more frequent major cycles
         niter = 1000000,    # try 50000 for single broad spw
         cycleniter = 20000,
         mask = 'circle[[121pix, 96pix],50pix]',
         threshold='0.005Jy', #
         restoringbeam='common',
         weighting = 'briggs',
         robust = 0.5,
         gridder = 'standard',
         pbcor = True,
         interactive = True
         )