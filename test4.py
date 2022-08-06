
import plotly.graph_objects as go

import pandas as pd
import numpy as np


# days = np.linspace(0,7,29)
# days = [0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5, 2.75, 3.0, 3.25, 3.5, 3.75, 4.0, 4.25, 4.5, 4.75, 5.0, 5.25, 5.5, 5.75, 6.0, 6.25, 6.5, 6.75, 7.0]

dataset = pd.read_csv('trainpath.csv')

days = []
for k in range(len(dataset['day'])):
    if dataset['day'][k] not in days:
        days.append(dataset['day'][k])

t1 = [-1, 0, 1, 1, 1, 0, -1, -1, -1]
k1 = [-20, -20, -20, 0, 20, 20, 20, 0, -20]

# make list of trains
trains = []
for train in dataset["train"]:
    if train not in trains:
        trains.append(train)

# make figure
fig_dict = {
    "data": [go.Scatter(x=t1, y=k1,
                     mode="lines",
                     line=dict(width=2, color="blue")),
            go.Scatter(x=t1, y=k1,
                     mode="lines",
                     line=dict(width=2, color="blue"))],
    "layout": {},
    "frames": []
}

# fill in most of layout

fig_dict['layout']['title'] = {'text':'Train Animation'}
fig_dict["layout"]["xaxis"] = {"range": [-10, 10], "title": "xlocation", 'autorange':False, 'zeroline':False}
fig_dict["layout"]["yaxis"] = {"range": [-22, 22], "title": "ylocation", 'autorange':False, 'zeroline':False}
fig_dict["layout"]["hovermode"] = "closest"
fig_dict["layout"]["updatemenus"] = [
    {
        "buttons": [
            {
                "args": [None, {"frame": {"duration": 500, "redraw": False},
                                "fromcurrent": True, "transition": {"duration": 300,
                                                                    "easing": "quadratic-in-out"}}],
                "label": "Play",
                "method": "animate"
            },
            {
                "args": [[None], {"frame": {"duration": 0, "redraw": False},
                                  "mode": "immediate",
                                  "transition": {"duration": 0}}],
                "label": "Pause",
                "method": "animate"
            }
        ],
        "direction": "left",
        "pad": {"r": 10, "t": 87},
        "showactive": False,
        "type": "buttons",
        "x": 0.1,
        "xanchor": "right",
        "y": 0,
        "yanchor": "top"
    }
]

sliders_dict = {
    "active": 0,
    "yanchor": "top",
    "xanchor": "left",
    "currentvalue": {
        "font": {"size": 20},
        "prefix": "Day:",
        "visible": True,
        "xanchor": "right"
    },
    "transition": {"duration": 300, "easing": "cubic-in-out"},
    "pad": {"b": 10, "t": 50},
    "len": 0.9,
    "x": 0.1,
    "y": 0,
    "steps": []
}

# make data

day = 0
for train in trains:
    dataset_by_date = dataset[dataset['day']==day]
    dataset_by_date_and_train = dataset_by_date[dataset_by_date['train']==train]

    data_dict = {
        'x': list(dataset_by_date_and_train['x']),
        'y': list(dataset_by_date_and_train['y']),
        'mode': 'markers',
        'text': train,
        'marker': {
            'sizemode': 'area',
            'sizeref': 20,
            'size': 20,
            # 'size': list(dataset_by_date_and_train['quantity'])  # this section can be used to increase or decrease the marker size to reflect the material quantity            
        },
        'name': train
    }

    fig_dict['data'].append(data_dict)

# make frames

for day in days:
    frame={'data': [go.Scatter(x=t1, y=k1,
                     mode="lines",
                     line=dict(width=2, color="blue")),
                    go.Scatter(x=t1, y=k1,
                     mode="lines",
                     line=dict(width=2, color="blue"))], 'name':str(day)}
    for train in trains:
        dataset_by_date = dataset[dataset['day'] == day]
        dataset_by_date_and_train = dataset_by_date[dataset_by_date['train'] == train]

        data_dict = {
            'x': list(dataset_by_date_and_train['x']),
            'y': list(dataset_by_date_and_train['y']),
            'mode': 'markers',
            'text': train,
            'marker': {
                'sizemode': 'area',
                'sizeref': 20,
                'size': 20,
                # 'size': list(dataset_by_date_and_train['quantity'])  # this section can be used to increase or decrease the marker size to reflect the material quantity            
        },
        'name': train
        }
        frame['data'].append(data_dict)

    fig_dict['frames'].append(frame)

    slider_step = {'args': [
        [day],
        {'frame': {'duration':300, 'redraw':False},
        'mode': 'immediate',
        'transition': {'duration':3000}}
    ],
        'label': day,
        'method': 'animate'}
    sliders_dict["steps"].append(slider_step)
    if day == 7:
        print('H')

fig_dict["layout"]["sliders"] = [sliders_dict]

fig = go.Figure(fig_dict)

fig.show()