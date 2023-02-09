import pandas as pd

def read_chromatogram(fpath):
    raw_data = pd.read_excel(fpath, header = 1)
    curves = raw_data.columns[::2].values
    curves_2x = raw_data.columns.values.copy()
    curves_2x[1::2] = curves
    curvelabels = [label.split('_')[-1] for label in curves_2x]
    title = raw_data.columns[::2].values[0].split(':')[0]
    units = [unit.strip() for unit in raw_data.iloc[0].values]
    cols = list(zip(*[curvelabels, units]))
    c = pd.MultiIndex.from_tuples(cols, names = ['curve', 'unit'])
    data = pd.DataFrame(data=raw_data.iloc[1:].values, columns = c)
    return data, curvelabels, title