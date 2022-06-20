# relion-helper-scripts
A collection of scripts to help with RELION cryo-EM data processing

## classXD_particle_distribution_by_iter_03.py
for reading a *_data.star file and plotting the particle distribution per iteration
can be used for either Class2D or Class3D in Relion
![Track particle distribution among classes per iteration](/images/plot_class_distribution_per_iteration.jpg)


## make_starfile_01.py
Convert a cryoDRGN particle subset into a RELION star file maintaining the original Relion particle paths

## topaz_loss_01.py
Visualise the loss over every iteration during Topaz training in RELION4
![Loss over Topaz training iterations](/images/topaz_loss.png)
