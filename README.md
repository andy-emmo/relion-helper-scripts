# relion-helper-scripts
A collection of scripts to help with RELION cryo-EM data processing

## class2D_images_01.py
show the 2d class averages for each iteration
use imagemagick to downsample/make a gif:
```
mogrify -resize 50% *.png
convert -delay 20 -loop 0 *.png 2d_classes.gif
```
![Class averages per iteration as images](/images/2d_classes.gif)

## classXD_particle_distribution_by_iter_03.py
for reading a *_data.star file and plotting the particle distribution per iteration
can be used for either Class2D or Class3D in Relion
![Track particle distribution among classes per iteration](/images/plot_class_distribution_per_iteration.jpg)

## classXD_particle_distribution_histogram_02.py
for reading a *_data.star file and getting a histogram of particle distributions
![Histogram(s) of particle distribution among classes](/images/class_counts_job323_run_ct25_it043_data.star.png)

## make_starfile_01.py
Convert a cryoDRGN particle subset into a RELION star file maintaining the original Relion particle paths

## topaz_loss_01.py
Visualise the loss over every iteration during Topaz training in RELION4
![Loss over Topaz training iterations](/images/topaz_loss.png)
