"""
for reading a *_data.star file and plotting the particle distribution per iteration
can be used for either Class2D or Class3D in Relion
"""


def parse_star(fn, test=0):
    # Self-defining Text Archive and Retrieval
    # convert a star file into a python dict
    f = open(fn)
    data = f.read()
    f.close()
    # store each data group e.g., data_optics, data_particles, PDB info (for mmCIF), etc.
    # for Relion star files, there are generally many data groups
    # in mmCIF files, there is usually only one, which contains the entire PDB information.
    all_data = {}
    # in each data dict, any '_' entries that have only one associated data point will be represented on a single line
    # any '_' entries with more than one associated data point will be in a loop
    # each '_' entry will get its own dict, with a list to store the data points.
    this_data_name = ''
    this_data = {}
    in_loop = False  # to keep track of whether we are in a loop or not
    # start the parse
    data = data.split('\n')
    # if testing, take only the first 'test' number of lines
    if test:
        data = data[:test]
    # go through each line
    for d in data:
        # if it is a blank line or it begins with a hash, ignore it
        if len(d) < 2 or d[0] == '#':
            pass
        else:
            if 'data' in d[:5]:
                # we have a new data group
                if len(this_data):
                    all_data[this_data_name] = this_data
                this_data = {}
                this_data_name = d.replace(' ', '')  # there shouldn't be any whitespace, but we'll check
            elif 'loop_' in d:
                in_loop = True
            elif d[0] == '_':
                if in_loop:
                    # we have the key, now create an empty list to store the values
                    # sometimes there is a comment
                    d = d.split('#')[0]
                    d = d.replace(' ', '')
                    this_data[d] = []
                else:
                    # not in a loop
                    # a key-value pair is split by whitespace
                    s = [x for x in d.split(' ') if len(x) > 0]
                    #print(s)
                    this_data[s[0]] = [s[1]]
            else:
                # if we were in a loop, we are no longer
                if in_loop:
                    in_loop = False
                    these_keys = list(this_data.keys())

                # this will be the actual data
                # split by whitespace
                # mmCIFs will have some entries in quotes... this will break
                data_line = [x for x in d.split(' ') if len(x) > 0]
                #print(data_line)
                for n, dl in enumerate(data_line):
                    this_data[these_keys[n]].append(dl)
    all_data[this_data_name] = this_data
    return all_data


def get_class_distribution(star_data):
    #print('doing class distribution')
    class_ids = []
    for k in star_data.keys():
        #print(k)
        if k == 'data_particles':
            particles = star_data[k]
            #print(particles.keys())
            particle_data = particles['data']
            for p in particle_data:
                #print(p)
                class_ids.append(int(p[2]))
    #print(class_ids)
    #print(max(class_ids))
    class_id = []
    class_count = []
    for i in range(1, max(class_ids) + 1):
        #print(i, class_ids.count(i))
        class_id.append(i)
        class_count.append(class_ids.count(i))
    return class_id, class_count
    

def plot_particle_distribution(base_dir, out_dir):
    import matplotlib.pyplot as plt
    import numpy as np
    import os
    
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    # list all the model.star files in the directory
    model_star = sorted([x for x in os.listdir(base_dir) if 'model.star' in x])
    print(model_star)
    upper = 50.0
    resolution = []
    distribution = []
    for ms in model_star:
        it = [x for x in ms.split('_') if 'it' in x][0]
        print(it)
        it = it.replace('it', '')
        it = int(it)
        this_res = [it]
        this_dist = [it]
        star_contents = parse_star(os.path.join(base_dir,ms), test=500)
        #print(star_contents.keys())
        #print(star_contents['data_model_classes'].keys())
        #print(star_contents['data_model_classes']['_rlnEstimatedResolution'])
        for n in star_contents['data_model_classes']['_rlnClassDistribution']:
            this_dist.append(float(n))
        for n in star_contents['data_model_classes']['_rlnEstimatedResolution']:
            if n != 'inf':
                num = float(n)
                if num > upper:
                    num = upper
                this_res.append(num)
            else:
                this_res.append(upper)
        distribution.append(this_dist)
        resolution.append(this_res)
    # make figure
    fig, ax = plt.subplots(2, 1, sharex='col')
    
    # sort and make distribution array
    # then plot
    distribution = sorted(distribution, key=lambda x: x[0])
    distribution = np.array(distribution).T
    print(distribution.shape)
    style = ['-', '--', '-.', ':', ]
    for i in range(distribution.shape[0] - 1):
        #print(i%10, int(i/10), int(i/10)%len(style))
        ax[0].plot(distribution[0], distribution[i + 1],
                   label='Class {0}'.format(i + 1),
                   linestyle=style[int(i/10)%len(style)], color='C{0}'.format(i%10))

    # plot the resolution of the classes per iteration
    resolution = sorted(resolution, key=lambda x: x[0])
    res = np.array(resolution).T
    print(res.shape)
    for i in range(res.shape[0] - 1):
        ax[1].plot(res[0], res[i + 1],
                   label='Class {0}'.format(i + 1),
                   linestyle=style[int(i/10)%len(style)])
                   
    # make it all look pretty
    #ax[0].legend(loc='lower left')
    #ax[1].legend(loc='lower left', ncol=1, bbox_to_anchor=(1, 0.5))
    if distribution.shape[0] > 10:
        ax[1].legend(loc='upper center', ncol=4, bbox_to_anchor=(0.5, -0.3))
        plt.gcf().set_size_inches(6, 12)  # width, height
    else:
        ax[1].legend(loc='upper center', ncol=3, bbox_to_anchor=(0.5, -0.3))
        plt.gcf().set_size_inches(6, 6)
    ax[0].set_ylabel('Distribution')
    ax[1].set_ylabel('Resolution (Å)')
    ax[-1].set_xlabel('Iteration')
    plt.tight_layout(rect=(0., 0., 1., 0.95))  # (left, bottom, right, top)
    plt.suptitle(base_dir)
    plt.savefig(os.path.join(out_dir, 'aplot.png'))
    plt.savefig(os.path.join(base_dir, 'aplot.png'))
    plt.show()

    if 0:
        # use the corner plot to see correlation between particle distribution
        labels = []
        ticks = []
        print(distribution.shape)
        d = distribution[1:, int(distribution.shape[1]*0.75):]  # distribution[0] is the iteration number
        for i in range(d.shape[0]):
            ticks.append(i)
            labels.append("Class {0}".format(i+1))

        print(np.corrcoef(d))
        plt.imshow(np.corrcoef(d))
        yticks = plt.yticks()
        print(yticks)
        plt.yticks(ticks, labels)
        plt.xticks(ticks, labels, rotation=90)
        plt.tight_layout()
        plt.savefig(base_dir + 'apcplot.png')
        plt.show()

    if 0:
        # corner plot
        for i in range(d.shape[0]):
            labels.append("Class {0}".format(i+1))
        print(d.shape)
        fig = corner(d.T, labels=labels, show_titles=True)
        fig.set_size_inches(12, 12)
        plt.show()

if __name__ == '__main__':
    base_dir = '/media/soneya/SS07/rln_giardia_1/Class2D/job011'  # this is the path to the Class2D or Class3D job
    out_dir = './plots_class_dist'  # the directory you want to output your images to
    plot_particle_distribution(base_dir, out_dir)
    
    



