import pandas as pd


class RelativeStrengthIndex:
    def __init__(self, df):
        self.period = 14
        self.df = df

    def calculate(self):
        # Get the difference in price from the previous day
        delta = self.__calculate_delta()

        down, up = self.__calculate_up_down(delta)

        avg_gain, avg_loss = self.__calculate_avg_gain_loss(down, up)

        # Calculate RS
        rs = avg_gain / avg_loss

        rsi_df = self.__calculate_rsi(rs)

        return rsi_df

    def __calculate_rsi(self, rs):
        # Calculate RSI
        rsi = 100.0 - (100.0 / (1.0 + rs))
        rsi_df = pd.DataFrame()
        rsi_df['Close'] = self.df['Close']
        rsi_df['RSI'] = rsi
        return rsi_df

    def __calculate_avg_gain_loss(self, down, up):
        avg_gain = up.rolling(window=self.period).mean()
        avg_loss = abs(down.rolling(window=self.period).mean())
        return avg_gain, avg_loss

    def __calculate_up_down(self, delta):
        up = delta.copy()
        down = delta.copy()
        up[up < 0] = 0
        down[down > 0] = 0
        return down, up

    def __calculate_delta(self):
        delta = self.df['Close'].diff(1)
        delta = delta.dropna()
        return delta

    def show_rsi(self, plt, st, data):
        # Show the RSI
        fig = plt.figure(figsize=(13.2, 5))
        plt.title('RSI Plot')
        plt.plot(data.index, data['RSI'])
        plt.axhline(0, linestyle='--', alpha=0.5, color='gray')
        plt.axhline(10, linestyle='--', alpha=0.5, color='orange')
        plt.axhline(20, linestyle='--', alpha=0.5, color='green')
        plt.axhline(30, linestyle='--', alpha=0.5, color='red')
        plt.axhline(70, linestyle='--', alpha=0.5, color='red')
        plt.axhline(80, linestyle='--', alpha=0.5, color='green')
        plt.axhline(90, linestyle='--', alpha=0.5, color='orange')
        plt.axhline(100, linestyle='--', alpha=0.5, color='gray')
        st.pyplot(fig)
