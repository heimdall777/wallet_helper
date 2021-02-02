from models.record import Record


async def parse_df_to_records(df):
    return [
        Record(
            record_id=index,
            date=record[0],
            open_price=record[1],
            high_price=record[2],
            low_price=record[3],
            close_price=record[4],
            volume=record[5]
        ) for index, record in enumerate(df.values.tolist(), start=1)
    ]
