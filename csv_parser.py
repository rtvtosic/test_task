import pandas as pd
from datetime import datetime


def parse_data(path: str) -> list:
    data = pd.read_csv(path)
    formatted_data = []
    id = 0

    for row in data.itertuples():
        text = row.text
        created_date = row.created_date
        rubrics = row.rubrics

        # преобразование created_date в datetime
        formatted_created_date = datetime.strptime(created_date, "%Y-%m-%d %H:%M:%S")

        # преобразование rubrics из str в list[str]
        formatted_rubrics = [x.strip("'") for x in rubrics[1:-1].split(', ')]
        formatted_data.append((id, text, formatted_created_date, formatted_rubrics))
        id += 1
    
    return formatted_data


if __name__ == "__main__":
    # data = parse_data('posts.csv')
    # print(data)
    print(parse_data('posts.csv'))