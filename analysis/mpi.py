import os
import uuid

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from h2o_wave import ui


class MoneyFlowIndex:
    def __init__(self, df):
        self.period = 14
        self.df = df

    def calculate(self):
        typical_price = self.__calculate_typicaly_price(self.df)
        positive_mf, negative_mf = self.__calculate_money_flow(typical_price, self.df)

        # Calculate the money flow index
        mfi = self.__calculate_money_flow_index(negative_mf, positive_mf)

        mfi_df = pd.DataFrame(self.df[self.period:])
        mfi_df['MFI'] = mfi

        # Add new columns (Buy & Sell)
        mfi_df['Buy'] = self.__get_signal(mfi_df, 80, 20)[0]
        mfi_df['Sell'] = self.__get_signal(mfi_df, 80, 20)[1]

        return mfi_df

    def __get_signal(self, data, high, low):
        buy_signal = []
        sell_signal = []

        for k in range(len(data['MFI'])):
            if data['MFI'][k] > high:
                buy_signal.append(np.nan)
                sell_signal.append(data['Close'][k])
            elif data['MFI'][k] < low:
                buy_signal.append(data['Close'][k])
                sell_signal.append(np.nan)
            else:
                buy_signal.append(np.nan)
                sell_signal.append(np.nan)

        return buy_signal, sell_signal

    def __calculate_money_flow_index(self, negative_mf, positive_mf):
        return 100 * (np.array(positive_mf) / (np.array(positive_mf) + np.array(negative_mf)))

    def __calculate_typicaly_price(self, df):
        # Typical price
        return (df.Close + df.High + df.Low) / 3

    def __calculate_money_flow(self, typical_price_param, df):
        money_flow = typical_price_param * df.Volume
        # Get all of the positive and negative money flows
        positive_flow = []
        negative_flow = []
        for i in range(1, len(typical_price_param)):
            if typical_price_param[i] > typical_price_param[i - 1]:
                positive_flow.append(money_flow[i - 1])
                negative_flow.append(0)
            elif typical_price_param[i] < typical_price_param[i - 1]:
                positive_flow.append(0)
                negative_flow.append(money_flow[i - 1])
            else:
                positive_flow.append(0)
                negative_flow.append(0)
        # Get all of the positive and negative money flow with the time period
        posit_mf = []
        negat_mf = []
        for i in range(self.period - 1, len(positive_flow)):
            posit_mf.append(sum(positive_flow[i + 1 - self.period: i + 1]))
        for i in range(self.period - 1, len(negative_flow)):
            negat_mf.append(sum(negative_flow[i + 1 - self.period: i + 1]))

        return posit_mf, negat_mf

    async def show_mpi(self, q, data):
        # Show the Money Flow Index
        mfi_df = pd.DataFrame(data, columns=['MFI'])

        q.page['mfi_plot'] = ui.markdown_card(box='content', title='Money FLow Index', content='')

        # Render plot
        plt.style.use('seaborn')
        plt.figure(figsize=(13.2, 5))
        plt.plot(mfi_df.MFI, label='MFI')
        plt.axhline(10, linestyle='--', color='orange')
        plt.axhline(20, linestyle='--', color='blue')
        plt.axhline(80, linestyle='--', color='blue')
        plt.axhline(90, linestyle='--', color='orange')
        plt.title(f'MFI')
        plt.ylabel('MFI Values')
        image_filename = f'{str(uuid.uuid4())}.png'
        plt.savefig(image_filename)

        # Upload
        image_path, = await q.site.upload([image_filename])

        # Clean up
        os.remove(image_filename)

        # Display our plot in our markdown card
        q.page['mfi_plot'].content = f'![plot]({image_path})'

    async def show_close_price_plot_with_signals(self, q, data):
        q.page['close_price_plot'] = ui.markdown_card(box='content', title='Close Price', content='')

        # Render plot
        plt.style.use('seaborn')
        plt.figure(figsize=(13.2, 5))
        plt.plot(data.Close, label='Close Price', alpha=0.5)
        plt.scatter(data.index, data.Buy, color='green', label='Buy Signal', marker='^', alpha=1)
        plt.scatter(data.index, data.Sell, color='red', label='Sell Signal', marker='v', alpha=1)
        plt.title(f'Close Price')
        plt.xlabel('Date')
        plt.ylabel('Close Price')
        plt.legend(loc='upper left')
        image_filename = f'{str(uuid.uuid4())}.png'
        plt.savefig(image_filename)

        # Upload
        image_path, = await q.site.upload([image_filename])

        # Clean up
        os.remove(image_filename)

        # Display our plot in our markdown card
        q.page['close_price_plot'].content = f'![plot]({image_path})'
