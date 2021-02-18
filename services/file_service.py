import pandas as pd


class FileService:

    @staticmethod
    def upload(uploaded_file):
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            df.dropna(inplace=True)
            # Set date as the index to have the same DF as from Yahoo API
            return df.set_index(pd.DatetimeIndex(df['Date']).values)
        else:
            return pd.DataFrame()
