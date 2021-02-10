class Record:
    def __init__(self, record_id: int, date: str, open_price: float, high_price: float, low_price: float,
                 close_price: float, volume: float):
        self.volume = volume
        self.close_price = close_price
        self.low_price = low_price
        self.high_pirce = high_price
        self.open_price = open_price
        self.date = date
        self.record_id = f'R{record_id}'



