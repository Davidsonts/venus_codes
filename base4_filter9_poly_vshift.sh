#!/bin/bash
alias echo "echo > /dev/null"
# run up the STARLINK software
kappa
smurf
# fit the largest sinusoid, order 4, amplitude is a few K
# the intended interval is -123,123 km/s
# outside this range, the end pixels have been previously set to bad (using
"chpix")
mfittrend fittype=poly order=4 subtract=true axis=1 in=fullband_1 out=base4_1
ranges='"-123,123"'
mfittrend fittype=poly order=4 subtract=true axis=1 in=fullband_2 out=base4_2
\\
mfittrend fittype=poly order=4 subtract=true axis=1 in=fullband_3 out=base4_3
\\
mfittrend fittype=poly order=4 subtract=true axis=1 in=fullband_4 out=base4_4
\\
mfittrend fittype=poly order=4 subtract=true axis=1 in=fullband_5 out=base4_5
\\
mfittrend fittype=poly order=4 subtract=true axis=1 in=fullband_6 out=base4_6
\\
mfittrend fittype=poly order=4 subtract=true axis=1 in=fullband_7 out=base4_7
\\
mfittrend fittype=poly order=4 subtract=true axis=1 in=fullband_8 out=base4_8
\\
mfittrend fittype=poly order=4 subtract=true axis=1 in=fullband_9 out=base4_9
\\
mfittrend fittype=poly order=4 subtract=true axis=1 in=fullband_10 out=base4_
10 \\
mfittrend fittype=poly order=4 subtract=true axis=1 in=fullband_11 out=base4_
11 \\
# also fit a constant level (by sub-scan) to use as continuum later on
mfittrend fittype=poly order=0 subtract=false axis=1 in=fullband_1 out=cont_1
\\
mfittrend fittype=poly order=0 subtract=false axis=1 in=fullband_2 out=cont_2
\\
mfittrend fittype=poly order=0 subtract=false axis=1 in=fullband_3 out=cont_3
\\
mfittrend fittype=poly order=0 subtract=false axis=1 in=fullband_4 out=cont_4
\\
mfittrend fittype=poly order=0 subtract=false axis=1 in=fullband_5 out=cont_5
\\
mfittrend fittype=poly order=0 subtract=false axis=1 in=fullband_6 out=cont_6
\\
mfittrend fittype=poly order=0 subtract=false axis=1 in=fullband_7 out=cont_7
\\
mfittrend fittype=poly order=0 subtract=false axis=1 in=fullband_8 out=cont_8
\\
mfittrend fittype=poly order=0 subtract=false axis=1 in=fullband_9 out=cont_9
\\
mfittrend fittype=poly order=0 subtract=false axis=1 in=fullband_10 out=cont_
10 \\
mfittrend fittype=poly order=0 subtract=false axis=1 in=fullband_11 out=cont_
11 \\
# now fit the shallow ripple: first filter data over broad box
block estimator=mean box="[1024,1,1]" in=base4_1 out=filt1024_1
block estimator=mean box="[1024,1,1]" in=base4_2 out=filt1024_2
block estimator=mean box="[1024,1,1]" in=base4_3 out=filt1024_3
block estimator=mean box="[1024,1,1]" in=base4_4 out=filt1024_4
block estimator=mean box="[1024,1,1]" in=base4_5 out=filt1024_5
block estimator=mean box="[1024,1,1]" in=base4_6 out=filt1024_6
block estimator=mean box="[1024,1,1]" in=base4_7 out=filt1024_7
block estimator=mean box="[1024,1,1]" in=base4_8 out=filt1024_8
block estimator=mean box="[1024,1,1]" in=base4_9 out=filt1024_9
block estimator=mean box="[1024,1,1]" in=base4_10 out=filt1024_10
block estimator=mean box="[1024,1,1]" in=base4_11 out=filt1024_11
# fit this shallow sinuosoid to filtered data, order 9
mfittrend fittype=poly order=9 subtract=false axis=1 in=filt1024_1 out=poly9_
1 \\
mfittrend fittype=poly order=9 subtract=false axis=1 in=filt1024_2 out=poly9_
2 \\
mfittrend fittype=poly order=9 subtract=false axis=1 in=filt1024_3 out=poly9_
3 \\
mfittrend fittype=poly order=9 subtract=false axis=1 in=filt1024_4 out=poly9_
4 \\
mfittrend fittype=poly order=9 subtract=false axis=1 in=filt1024_5 out=poly9_
5 \\
mfittrend fittype=poly order=9 subtract=false axis=1 in=filt1024_6 out=poly9_
6 \\
mfittrend fittype=poly order=9 subtract=false axis=1 in=filt1024_7 out=poly9_
7 \\
mfittrend fittype=poly order=9 subtract=false axis=1 in=filt1024_8 out=poly9_
8 \\
mfittrend fittype=poly order=9 subtract=false axis=1 in=filt1024_9 out=poly9_
9 \\
mfittrend fittype=poly order=9 subtract=false axis=1 in=filt1024_10 out=poly9
_10 \\
mfittrend fittype=poly order=9 subtract=false axis=1 in=filt1024_11 out=poly9
_11 \\
# subtract the fitted shallow sinusoid
sub in1=base4_1 in2=poly9_1 out=base4+9_1
sub in1=base4_2 in2=poly9_2 out=base4+9_2
sub in1=base4_3 in2=poly9_3 out=base4+9_3
sub in1=base4_4 in2=poly9_4 out=base4+9_4
sub in1=base4_5 in2=poly9_5 out=base4+9_5
sub in1=base4_6 in2=poly9_6 out=base4+9_6
sub in1=base4_7 in2=poly9_7 out=base4+9_7
sub in1=base4_8 in2=poly9_8 out=base4+9_8
sub in1=base4_9 in2=poly9_9 out=base4+9_9
sub in1=base4_10 in2=poly9_10 out=base4+9_10
sub in1=base4_11 in2=poly9_11 out=base4+9_11
# select the region for close baselining
# intended region is -36 to +64 km/s
ndfcopy in="base4+9_1(3046:5963,,)" out=close_1
ndfcopy in="base4+9_2(3046:5963,,)" out=close_2
ndfcopy in="base4+9_3(3046:5963,,)" out=close_3
ndfcopy in="base4+9_4(3046:5963,,)" out=close_4

ndfcopy in="base4+9_5(3046:5963,,)" out=close_5
ndfcopy in="base4+9_6(3046:5963,,)" out=close_6
ndfcopy in="base4+9_7(3046:5963,,)" out=close_7
ndfcopy in="base4+9_8(3046:5963,,)" out=close_8
ndfcopy in="base4+9_9(3046:5963,,)" out=close_9
ndfcopy in="base4+9_10(3046:5963,,)" out=close_10
ndfcopy in="base4+9_11(3046:5963,,)" out=close_11
# determine the 8th order polynomials around the line at velocity of +13.8
(+/-0.3) km/s
# exclude line region, e.g. +-7 km/s use range: -36,6.8,20.8,64
mfittrend fittype=poly order=8 subtract=false axis=1 in=close_1 out=poly_1
mfittrend fittype=poly order=8 subtract=false axis=1 in=close_2 out=poly_2 \\
mfittrend fittype=poly order=8 subtract=false axis=1 in=close_3 out=poly_3 \\
mfittrend fittype=poly order=8 subtract=false axis=1 in=close_4 out=poly_4 \\
mfittrend fittype=poly order=8 subtract=false axis=1 in=close_5 out=poly_5 \\
mfittrend fittype=poly order=8 subtract=false axis=1 in=close_6 out=poly_6 \\
mfittrend fittype=poly order=8 subtract=false axis=1 in=close_7 out=poly_7 \\
mfittrend fittype=poly order=8 subtract=false axis=1 in=close_8 out=poly_8 \\
mfittrend fittype=poly order=8 subtract=false axis=1 in=close_9 out=poly_9 \\
mfittrend fittype=poly order=8 subtract=false axis=1 in=close_10 out=poly_10
\\
mfittrend fittype=poly order=8 subtract=false axis=1 in=close_11 out=poly_11
\\
# make the chunks of the continuum levels
ndfcopy in="cont_1(3046:5963,,)" out=contbit_1
ndfcopy in="cont_2(3046:5963,,)" out=contbit_2
ndfcopy in="cont_3(3046:5963,,)" out=contbit_3
ndfcopy in="cont_4(3046:5963,,)" out=contbit_4
ndfcopy in="cont_5(3046:5963,,)" out=contbit_5
ndfcopy in="cont_6(3046:5963,,)" out=contbit_6
ndfcopy in="cont_7(3046:5963,,)" out=contbit_7
ndfcopy in="cont_8(3046:5963,,)" out=contbit_8
ndfcopy in="cont_9(3046:5963,,)" out=contbit_9
ndfcopy in="cont_10(3046:5963,,)" out=contbit_10
ndfcopy in="cont_11(3046:5963,,)" out=contbit_11
# make the line-to-continuum ratios
maths "(ia+ic)/(ib+ic)-1" ia=close_1 ib=poly_1 ic=contbit_1 out=ltoc_1
maths "(ia+ic)/(ib+ic)-1" ia=close_2 ib=poly_2 ic=contbit_2 out=ltoc_2
maths "(ia+ic)/(ib+ic)-1" ia=close_3 ib=poly_3 ic=contbit_3 out=ltoc_3
maths "(ia+ic)/(ib+ic)-1" ia=close_4 ib=poly_4 ic=contbit_4 out=ltoc_4
maths "(ia+ic)/(ib+ic)-1" ia=close_5 ib=poly_5 ic=contbit_5 out=ltoc_5
maths "(ia+ic)/(ib+ic)-1" ia=close_6 ib=poly_6 ic=contbit_6 out=ltoc_6
maths "(ia+ic)/(ib+ic)-1" ia=close_7 ib=poly_7 ic=contbit_7 out=ltoc_7
maths "(ia+ic)/(ib+ic)-1" ia=close_8 ib=poly_8 ic=contbit_8 out=ltoc_8
maths "(ia+ic)/(ib+ic)-1" ia=close_9 ib=poly_9 ic=contbit_9 out=ltoc_9
maths "(ia+ic)/(ib+ic)-1" ia=close_10 ib=poly_10 ic=contbit_10 out=ltoc_10
maths "(ia+ic)/(ib+ic)-1" ia=close_11 ib=poly_11 ic=contbit_11 out=ltoc_11
# now align line:cont spectra in Venus velocity frame
# shifts are from topocentric frame, mid-point of observation
wcsslide ndf=ltoc_1 abs="[14.06,0,0]"
wcsslide ndf=ltoc_2 abs="[13.88,0,0]"
wcsslide ndf=ltoc_3 abs="[13.95,0,0]"
wcsslide ndf=ltoc_4 abs="[13.81,0,0]"

wcsslide ndf=ltoc_5 abs="[13.87,0,0]"
wcsslide ndf=ltoc_6 abs="[13.49,0,0]"
wcsslide ndf=ltoc_7 abs="[13.54,0,0]"
wcsslide ndf=ltoc_8 abs="[13.61,0,0]"
wcsslide ndf=ltoc_9 abs="[13.68,0,0]"
wcsslide ndf=ltoc_10 abs="[13.76,0,0]"
wcsslide ndf=ltoc_11 abs="[13.86,0,0]"
# now co-add the scans, into 1 pixel, generating variance by channel,
weighting scans by Tsys (or not)
makecube autogrid=true pixsize=600 genvar=spread sparse=false badmask=and
specunion=false inweight=true in="ltoc_*.sdf"