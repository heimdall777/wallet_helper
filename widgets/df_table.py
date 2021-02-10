from h2o_wave import ui


class DataFrameTable:
    def __init__(self):
        self.columns = [
            ui.table_column(name='date', label='Date', sortable=True, data_type='time'),
            ui.table_column(name='open', label='Open', sortable=True, data_type='number'),
            ui.table_column(name='high', label='High', sortable=True, data_type='number'),
            ui.table_column(name='low', label='Low', sortable=True, data_type='number'),
            ui.table_column(name='close', label='Close', sortable=True, data_type='number'),
            ui.table_column(name='volume', label='Volume', sortable=True, data_type='number'),
        ]

    def show(self, records):
        return ui.table(
            name='Data',
            columns=self.columns,
            rows=[ui.table_row(
                name=record.record_id,
                cells=[record.date, record.open_price, record.high_pirce, record.low_price, record.close_price,
                       record.volume]
            ) for record in records],
            downloadable=True,
            resettable=True,
            height='600px'
        )
