import random

def connect_sequential_stations(graph, df):
    df_sorted = df.sort_values(['line', 'num'])
    for i in range(len(df_sorted) - 1):
        curr = df_sorted.iloc[i]
        next_ = df_sorted.iloc[i + 1]

        # If on the same line and sequential in number
        if curr['line'] == next_['line'] and next_['num'] - curr['num'] == 1:
            weight = random.randint(2, 8)
            graph.connect(curr['code'], next_['code'], weight=weight)

def connect_transfer_stations(graph, df, transfer_weight=5):
    # Group by station name (interchanges)
    grouped = df.groupby('name')
    for name, group in grouped:
        codes = group['code'].tolist()
        # Only connect if there's more than 1 code (i.e., a transfer)
        if len(codes) > 1:
            for i in range(len(codes)):
                for j in range(i + 1, len(codes)):
                    graph.connect(codes[i], codes[j], weight=transfer_weight)
