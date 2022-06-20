
""" for reading a *_data.star file and getting a histogram of particle distributions
    used within RELION project directory "Class3D",
    command line argument is the job number"""


def save_data_loop(all_data, this_data_name, this_data, this_loop):
    # save the data that has been collected
    all_data[this_data_name] = {'loop': this_loop, 'data': this_data}
    return all_data


def parse_star(fn, test=False):
    # convert a star file into a python dict and vice versa
    f = open(fn)
    data = f.read()
    f.close()
    # store each data group e.g., data_optics, data_particles, etc.
    all_data = {}
    this_data_name = ''
    this_data = []
    this_loop = []
    # each data group has a field description beginning with loop
    # split the data by newline
    data = data.split('\n')
    # if testing, take only the first few lines
    if test:
        data = data[:200]
    # go through each line
    # if it is a blank line or it begins with a hash, ignore it
    for d in data:
        if len(d) < 2 or d[0] == '#':
            pass
        else:
            if 'data' in d[:5]:
                # we have a new data group
                if len(this_loop):
                    save_data_loop(all_data, this_data_name, this_data, this_loop)
                this_data = []
                this_loop = []
                this_data_name = d
            elif 'loop_' in d:
                pass
            elif '_rln' in d[:5]:
                #print(d)
                this_loop.append(d)
            else:
                # this will be the actual data
                # split by whitespace
                data_line = [x for x in d.split(' ') if len(x) > 0]
                #print(data_line)
                this_data.append(data_line)
    save_data_loop(all_data, this_data_name, this_data, this_loop)
    #print(all_data)
    return all_data


def get_class_distribution(star_data, relion_ver='31'):
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
                # should make this look for the index of '_rlnClassNumber'
                if relion_ver == '31':
                    class_ids.append(int(p[3]))  # for relion 3.1
                else:
                    class_ids.append(int(p[2]))  # for relion 3.0
    #print(class_ids)
    #print(max(class_ids))
    class_id = []
    class_count = []
    for i in range(1, max(class_ids) + 1):
        #print(i, class_ids.count(i))
        class_id.append(i)
        class_count.append(class_ids.count(i))
    return class_id, class_count
    

def class_distribution_histogram(base_dir, out_dir):
    import matplotlib.pyplot as plt
    import numpy as np
    import os
    
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    
    fns = []
    if len(base_dir):
        fns = sorted([x for x in os.listdir(base_dir) if 'data.star' in x])
    
    for fn in fns:
        this_fn = os.path.join(base_dir, fn)
        print(this_fn)
        out_fn = os.path.join(out_dir, fn.replace('.star', '.png'))
        print(out_fn)
        if os.path.exists(out_fn):
            print('png already here, skipping')
        else:
            d = parse_star(this_fn, test=False)
            cid, count = get_class_distribution(d)
            plt.bar(cid, count)
            plt.xlabel('Class Number')
            plt.ylabel('Number of Particles')
            total = np.sum(count)
            for n, cn in enumerate(count):
                plt.text(n + 1, cn, '{1:0.1f}k\n{0:0.1f}%'.format(cn * 100 / total, cn / 1000), ha='center', va='bottom')
            plt.tight_layout()
            ax = plt.gca()
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            head, tail = os.path.split(this_fn)
            job_number = base_dir.split('/')[-1].replace('job', '')
            #plt.savefig('./class_counts_{0}'.format(tail + '.png'), dpi=150)
            if 'ct' in tail:
                plt.suptitle('Job {0} Iteration {1}'.format(job_number, tail.split('_')[2].replace('it','')))
            else:
                plt.suptitle('Job {0} Iteration {1}'.format(job_number, tail.split('_')[1].replace('it','')))
            plt.tight_layout(rect=(0, 0, 1, 0.95))  # (left, bottom, right, top)
            plt.gcf().set_size_inches(max(cid)/2., 6.)
            plt.savefig(out_fn, dpi=150)
            #plt.show()
            plt.close('all')


if __name__ == '__main__':
    base_dir = '/media/soneya/SS07/rln_giardia_1/Class2D/job011'  # this is the path to the Class2D or Class3D job
    out_dir = './plots_class_dist_histo'  # the directory you want to output your images to
    class_distribution_histogram(base_dir, out_dir)



