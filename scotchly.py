import scipy.io
from flask import Flask, request, render_template

# configuration
DEBUG = True
# The data file contains a correlation matrix of 87 different whiskies, 
# and a list of corresponding distillery names. The matrix
# is symmetric, with each entry i,j == j,i and represents a measure of
# similarity between the two samples.
DATA = scipy.io.loadmat('whisky.mat')
# string array imports from matlab nests the strings in layers of arrays
DATA['whiskynames'] = [str(x[0][0]) for x in DATA['whiskynames']]

# create our little application
app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/', methods=['GET', 'POST'])
def show_whisky():
    # show suggestions for selected whisky
    data = app.config['DATA']
    names = data['whiskynames']
    if request.method == 'POST':
        # get the index of the selected whisky
        name_idx = names.index(request.form['whisky'])
        # extract the row of scores pertaining to the selected whisky
        scores = data['whiskypcc'][name_idx]
        # bind scores to their names, so that we can keep track when we sort
        associated_scores = [(scores[i], names[i]) for i in range(len(scores))]
        associated_scores.sort(reverse=True)
        ordered_scores, ordered_names = zip(*associated_scores)
        # the highest correlated entry will always be itself, so skip frist match
        return render_template('suggest.html', names=names, selected=names[name_idx], suggestions=ordered_names[1:6])
    else:
        # just present the user with all the available whiskey choices
        return render_template('main.html', names=names, selected=names[0])

if __name__ == '__main__':
    app.run()