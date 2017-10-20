# Goal of this file is to take an image and a topography dataset and make some 3D representation

import os
import plotly.offline as po
import plotly.tools as pt
import plotly.graph_objs as go
import json
import pickle
import numpy
from data.subsample_matrix import subsample_matrix


with open('data/paired_data.json', 'r') as f:
    data = json.load(f)


for i, scene in enumerate(data):
    i = 15
    scene = data[i]
    # Load the topographical information in matrix form. The pickle file should have been created by
    # convert_las_to_matrix.py
    pickle_filename = 'data/' + str(i) + '/' + scene[0]['displayId'] + '.pickle'
    print(pickle_filename)
    if os.path.isfile(pickle_filename) is False:
        continue
    z_data = pickle.load(open(pickle_filename, 'rb'))

    # scale matrix down to something that can be reasonably loaded in an html page
    matrix_size = 300
    m = subsample_matrix(z_data, matrix_size)

    # Create a surface plot
    test = pickle.load(open('test.pickle', 'rb'))
    plot_data = [go.Surface(z=m), go.Surface(z=test)]

    # Set up the camera so that the orientation of the surface is similar to the orientation of the associated image
    camera = dict(
            up=dict(x=1, y=0, z=0),
            center=dict(x=0, y=0, z=0),
            eye=dict(x=0, y=-1.6, z=1.35)
    )

    # Grab the image associated with the lidar dataset to display next to the 3d surface plot. For now, images will be
    # stored in my github
    image_filename = 'cropped.jpg'
    image_source = 'https://raw.githubusercontent.com/nbelakovski/topography_neural_net/master/data/' + str(i) + '/' + \
                   image_filename
    layout = go.Layout(
        title='Elevations near Glacier Peak, WA',
        autosize=True,
        images=
        [
            dict
            (
                source=image_source,
                xref="paper", yref="paper",
                x=-0.07, y=0.83,
                sizing="stretch",
                sizex=0.4, sizey=0.7, layer="below",
                xanchor='left', yanchor='top'
            )
        ],
        annotations=[
            dict(
                x=.975,
                y=.5,
                xref='paper',
                yref='paper',
                text='TODO:' + '<br>' + 'Neural Net Topography' + '<br>' + 'Output Here',
                showarrow=False,
                font=dict(
                        size=36,
                )
            )
        ],
    )

    # Set up subplots. One for the lidar image, next for the original data, next for the machine learned data
    # The first subplot isn't actually used - the image is carefully placed to take up that slot
    fig = pt.make_subplots(1, 3, specs=[[{'is_3d': False}, {'is_3d': True}, {'is_3d': True}]])
    fig.append_trace(plot_data[0], 1, 2)
    fig.append_trace(plot_data[1], 1, 3)
    fig['layout'].update(layout)
    fig['layout'].update(scene1=dict(camera=camera))  # need to look at console output to determine which key to update

    # PLOT!
    a = po.plot(fig)
    print("Done")
    break
