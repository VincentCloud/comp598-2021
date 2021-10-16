
from bokeh.plotting import figure, curdoc
from bokeh.layouts import column
from bokeh.models import ColumnDataSource
import pandas as pd
from bokeh.models import CustomJS, Dropdown


def update_plot1(new_zip):
    print(
        f'stream_dict: {stream_dict} length of each entry: {len(stream_dict["x"])}, {len(stream_dict["y1"])}, {len(stream_dict["y2"])}, {len(stream_dict["y3"])}')
    stream_dict['y1'] = df[df['Zip Codes'] == new_zip.item].iloc[0].tolist()[1:10]
    data_src.stream(stream_dict, rollover=9)


def update_plot2(new_zip):
    print(
        f'stream_dict: {stream_dict} length of each entry: {len(stream_dict["x"])}, {len(stream_dict["y1"])}, {len(stream_dict["y2"])}, {len(stream_dict["y3"])}')
    stream_dict['y2'] = df[df['Zip Codes'] == new_zip.item].iloc[0].tolist()[1:10]
    data_src.stream(stream_dict, rollover=9)


bokeh_doc = curdoc()
bokeh_doc.title = 'Monthly Average Response Time Sorted By Zip Codes'

df = pd.read_csv(
    '/Users/vincenthuang/Development/Study/COMP598/COMP598/comp598-2021/hw4/submission_template/data/average.csv')
zip_codes = df['Zip Codes'].unique()

menu = [(f'{zip}', f'{zip}') for zip in zip_codes]

stream_dict = {
    'x': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept'],
    'y1': [0 for i in range(0, 9)],
    'y2': [0 for j in range(0, 9)],
    'y3': df[df['Zip Codes'] == 'all'].iloc[0].tolist()[1:10]
}

dropdown_zip1 = Dropdown(label="Zip Code 1", button_type="warning", menu=menu)
dropdown_zip1.js_on_event("menu_item_click", CustomJS(code="console.log('dropdown: ' + this.item, this.toString())"))

dropdown_zip2 = Dropdown(label="Zip Code 2", button_type="warning", menu=menu)
dropdown_zip2.js_on_event("menu_item_click", CustomJS(code="console.log('dropdown: ' + this.item, this.toString())"))

plot = figure(title='Monthly Average Response Time', x_axis_label='Month', y_axis_label='Response Time (hr)',
              x_range=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept'])

data_src = ColumnDataSource(stream_dict)
plot.line(x='x', y='y1', source=data_src, line_color='red', legend_label='Zip Code 1')
plot.line(x='x', y='y2', source=data_src, line_color='blue', legend_label='Zip Code 2')
plot.line(x='x', y='y3', source=data_src, line_color='green', legend_label='All Data')

dropdown_zip1.on_click(update_plot1)
dropdown_zip2.on_click(update_plot2)

bokeh_doc.add_root(column([dropdown_zip1, dropdown_zip2]))
bokeh_doc.add_root(column([plot]))
