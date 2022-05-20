import matplotlib.pyplot as plt

# the file name
fn = 'model_training.txt'
# open the file and read the data
f = open(fn)
data = f.read()
f.close()
# split by newline so we can iterate through every entry
data = data.split('\n')
# some lists to store stuff
epoch = []
ita = []
loss = []
# iterate through every line and grab the data
# ignore the first row
for d in data[1:]:
    # only if there is something written on this line
    if len(d):
        # what's here?
        print(d)
        # split by tab
        d = d.split('\t')
        print(d)
        # grab the data and turn into integer or float
        epoch.append(int(d[0]))
        ita.append(int(d[1]))
        loss.append(float(d[3]))
# plot it!
plt.scatter(ita, loss)
plt.show()
