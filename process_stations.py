import pandas as pd
from graph import Vertex
import re

def process_stations(csv_path='stations.csv', exclude_lines=['BP', 'PTC', 'STC']):
    data = pd.read_csv(csv_path)
    features = pd.DataFrame({
        'name': data['STN_NAME'],
        'code': data['STN_NO']
    })

    new_rows = []
    for i, row in features.iterrows():
        codes = row['code'].split('/')
        if len(codes) > 1:
            features.at[i, 'code'] = codes[0]
            for code in codes[1:]:
                new_rows.append([row['name'], code])

    features = pd.concat([features, pd.DataFrame(new_rows, columns=['name', 'code'])], ignore_index=True)

    features['line'] = features['code'].str.extract(r'([A-Z]+)')
    features['num'] = features['code'].str.extract(r'(\d+)')

    features.dropna(subset=['num'], inplace=True)
    features = features[~features['line'].isin(exclude_lines)]
    features['num'] = pd.to_numeric(features['num'], downcast='integer')

    features.sort_values(['line', 'num'], inplace=True)

    return features.reset_index(drop=True)

def build_station_vertices(features):
    metro = {}
    for _, row in features.iterrows():
        vertex = Vertex(row['code'])
        vertex.data = row['name']
        metro[row['code']] = vertex
    return metro
