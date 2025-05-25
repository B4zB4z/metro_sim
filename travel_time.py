import random

def connect_sequential_stations(graph, df):
    df_sorted = df.sort_values(['line', 'num'])
    for i in range(len(df_sorted) - 1):
        curr = df_sorted.iloc[i]
        next_ = df_sorted.iloc[i + 1]

        if curr['line'] == next_['line'] and next_['num'] - curr['num'] == 1:
            weight = random.randint(2, 8)
            graph.connect(curr['code'], next_['code'], weight=weight)

def connect_transfer_stations(graph, df, transfer_weight=5):
    grouped = df.groupby('name')
    for name, group in grouped:
        codes = group['code'].tolist()
        if len(codes) > 1:
            for i in range(len(codes)):
                for j in range(i + 1, len(codes)):
                    graph.connect(codes[i], codes[j], weight=transfer_weight)
