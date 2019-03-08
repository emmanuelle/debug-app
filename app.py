import numpy as np
import json
from skimage import io
from PIL import Image

import dash_canvas
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go

from dash_canvas.utils.parse_json import parse_jsonstring
from dash_canvas.utils.image_processing_utils import \
                                        superpixel_color_segmentation
from dash_canvas.utils.plot_utils import image_with_contour
from dash_canvas.utils.io_utils import image_string_to_PILImage, \
                                       array_to_data_url
from dash_canvas.components import image_upload_zone

# Image to segment and shape parameters
filename = './assets/dress.jpg'
img = io.imread(filename)
height, width, _ = img.shape
canvas_width = 500
canvas_height = round(height * canvas_width / width)
scale = canvas_width / width

app = dash.Dash(__name__)
server = app.server
app.config.suppress_callback_exceptions = False


app.layout = html.Div([
    html.Div([
        html.Div([
            dash_canvas.DashCanvas(
                id='canvas-bg',
                width=canvas_width,
                height=canvas_height,
                scale=scale,
                filename=filename,
                lineWidth=4,
                goButtonTitle='Remove background',
                hide_buttons=['line', 'zoom', 'pan'],
            ),
        ], className="six columns"),
        html.Div([
            html.Img(id='segmentation-bg',
                     src=array_to_data_url(np.zeros_like(img)),
                     width=canvas_width)
        ], className="six columns")],
        className="row")
        ])


@app.callback(Output('segmentation-bg', 'src'),
             [Input('canvas-bg', 'json_data')],)
def update_figure_upload(string):
    if string is None:
        raise PreventUpdate
    return array_to_data_url(img)


if __name__ == '__main__':
    app.run_server(debug=True)

