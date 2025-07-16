import numpy as np
import pandas as pd
import ta
from scipy import stats
import ta.others

from eda.helpers import StockOLHCV
from helpers import ProgressdownDecorator

class OutliersTransformer():
    """
    OutliersTransformer is a class designed to handle outliers in stock market data, specifically for open, low, high, close prices, and volume.
    The OutliersTransformer replaces 'Open' and  'Close' prices with mean of the other prices(if they are not out o the limits).
    'Low' prise is replaces by minimum of the oters and 'High' price are replaced by the maximum.
    'Volume' outliers are capped using IQR method with 1st quantile = `0.1`, 2d quantile = `0.9` quantile interval rate = `3.5`.
    Attributes:
        low_threshold (float): The lower z-score threshold for detecting outliers.
        high_threshold (float): The upper z-score threshold for detecting outliers.
        volume_quantile_range (tuple): The quantile range for volume capping.
        volume_interval_rate (float): The interval rate for volume capping.
        high_low_coeff (float): Coefficient used for adjusting high and low prices.
    Methods:
        fit(X):
            Fits the transformer to the data. Currently, it does nothing and returns self.
        transform(X):
            Transforms the data by handling outliers in open, low, high, close prices, and volume.
        _replace_by_mean(X, res, col):
            Replaces outliers in the specified column with the mean of non-outlier values.
        _get_other_cols_and_outliers(col):
            Returns the other columns and the indices of outliers for the specified column.
        _get_cols_non_outliers_mask(idx, cols, multiplier=1.5):
            Returns a mask indicating non-outlier values for the specified columns.
        _append_row_to_remove(idx):
            Appends the specified row index to the list of rows to remove.
        _capping_volume(s):
            Caps the volume outliers using the IQR method.
        fit_transform(X):
            Fits the transformer and then transforms the data.
    """
    def __init__(self, low_threshold=-4, high_threshold=5, high_low_coeff=0.99, volume_quantile_range=(0.1, 0.9), volume_interval_rate=3.5):
        self.low_threshold = low_threshold
        self.high_threshold = high_threshold
        self.volume_quantile_range = volume_quantile_range
        self.volume_interval_rate = volume_interval_rate
        self._olhc = ['open', 'low', 'high', 'close']
        self.high_low_coeff = high_low_coeff
        self._row_idx_to_remove = None
    def fit(self, X):
        return self
    def transform(self, X):
        res=X.copy()
        self._z_scores = StockOLHCV(res.groupby('Name').transform(stats.zscore))
        #open
        res = self._replace_by_mean(X, res, 'open')
        #close
        res = self._replace_by_mean(X, res, 'close')
        #high
        other_cols, outliers_indexes = self._get_other_cols_and_outliers('high')
        for idx in outliers_indexes:
            not_outliers_prices_mask = self._get_cols_non_outliers_mask(idx, other_cols)
            if not_outliers_prices_mask.sum() == 0: # there are no non-outliers prices in the row
                self._append_row_to_remove(idx)
            else:
                res.loc[idx, 'high'] = (X.loc[idx, other_cols])[self._get_cols_non_outliers_mask(idx, other_cols)].max()/self.high_low_coeff
        #low
        other_cols, outliers_indexes = self._get_other_cols_and_outliers('low')
        for idx in outliers_indexes:
            not_outliers_prices_mask = self._get_cols_non_outliers_mask(idx, other_cols)
            if not_outliers_prices_mask.sum() == 0: # there are no non-outliers prices in the row
                self._append_row_to_remove(idx)
            else:
                res.loc[idx, 'low'] = self.high_low_coeff*(X.loc[idx, other_cols])[self._get_cols_non_outliers_mask(idx,other_cols)].min()
        #volume
        res['volume'] = res.groupby('Name')['volume'].transform(self._capping_volume)
        if self._row_idx_to_remove is not None:
            return res.drop(index=self._row_idx_to_remove)
        else:
            return res


    def _replace_by_mean(self, X, res, col):
        other_cols, outliers_indexes = self._get_other_cols_and_outliers(col)
        for idx in outliers_indexes:
            not_outliers_prices_mask = self._get_cols_non_outliers_mask(idx, other_cols)
            if not_outliers_prices_mask.sum() == 0: # there are no non-outliers prices in the row
                self._append_row_to_remove(idx)
                return res # do not change the row
            res.loc[idx, col] = (X.loc[idx, other_cols])[not_outliers_prices_mask].mean()
        return res   

    def _get_other_cols_and_outliers(self, col):
        other_cols = [c for c in self._olhc if c != col]
        outliers_indexes = self._z_scores[(self._z_scores[col] < self.low_threshold) | (self._z_scores[col] > self.high_threshold)].index
        return other_cols, outliers_indexes
    
    def _get_cols_non_outliers_mask(self,idx, cols, multiplier=1.5):
        other_scores = self._z_scores.loc[idx, cols]
        not_outliers_prices_mask = (other_scores >= self.low_threshold) & (other_scores <= self.high_threshold)
        if not_outliers_prices_mask.sum() == 0: # there are no non-outliers prices in the row
            not_outliers_prices_mask = (other_scores >= multiplier * self.low_threshold) & (other_scores <= multiplier * self.high_threshold)
        return not_outliers_prices_mask
    
    def _append_row_to_remove(self, idx):
        if self._row_idx_to_remove is None:
            self._row_idx_to_remove = idx
        else:
            self._row_idx_to_remove.append(idx)
    
    def _capping_volume(self, s, ):
        # Capping outliers using IQR method
        Q1 = s.quantile(self.volume_quantile_range[0])
        Q3 = s.quantile(self.volume_quantile_range[1])
        IQR = self.volume_interval_rate * (Q3 - Q1)
        lower_bound = Q1 - IQR
        upper_bound = Q3 + IQR
        res = np.where(s < lower_bound, lower_bound, s)
        res = np.where(res > upper_bound, upper_bound, res)
        return res


    def fit_transform(self, X):
        self.fit(X)
        return self.transform(X)
    
@ProgressdownDecorator(5, lambda x: x.name) # the function is used with pandas GroupBy.apply method, so the argument has the name attribute
def create_features_old(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate various technical indicators and features from the given DataFrame.
    Parameters:
    df (pd.DataFrame): DataFrame containing stock data with columns 'close', 'high', 'low', and 'volume'.
    Returns:
    pd.DataFrame: DataFrame containing the calculated technical indicators and features.
    Features:
    - Volatility:
        - Bollinger Bands (mavg, width, hband_indicator, lband_indicator)
        - Average True Range (atr)
        - Keltner Channel (mband, width, hband_indicator, lband_indicator)
    - Momentum:
        - Relative Strength Index (rsi)
        - Awesome Oscillator (ao)
        - True Strength Index (tsi)
        - Percentage Volume Oscillator (pvo, pvo_signal)
    - Trend:
        - Moving Average Convergence Divergence (macd, macd_signal)
        - Aroon Indicator (Aroon_down, Aroon_up)
        - Commodity Channel Index (cci)
        - Weighted Moving Average (wma)
    - Volume:
        - Ease of Movement (ease_of_movement, sma_ease_of_movement)
        - Force Index (force_index)
        - Money Flow Index (money_flow_index)
        - Volume Weighted Average Price (volume_weighted_average_price)
    - Target:
        - Return between days D+1 and D+2 (target)
    """
    res = pd.DataFrame(index=df.index)
    #volatility
    indicator_bb = ta.volatility.BollingerBands(close=df["close"], window=20, window_dev=2) # window=20, window_dev=2 - default
    res['Bollinger_mavg'] = indicator_bb.bollinger_mavg()
    res['Bollinger_width'] = indicator_bb.bollinger_wband()
    res['Bollinger_hband_indicator'] = indicator_bb.bollinger_hband_indicator()
    res['Bollinger_lband_indicator'] = indicator_bb.bollinger_lband_indicator()
    res['atr'] = ta.volatility.average_true_range(high=df["high"], low=df["low"], close=df["close"], window=14)
    indicator_kc = ta.volatility.KeltnerChannel(high=df["high"], low=df["low"], close=df["close"], window=20, window_atr=10,original_version=True, multiplier=2)
    res['KeltnerChannel_mband'] = indicator_kc.keltner_channel_mband()
    res['KeltnerChannel_width'] = indicator_kc.keltner_channel_wband()
    res['KeltnerChannel_hband_indicator'] = indicator_kc.keltner_channel_hband_indicator()
    res['KeltnerChannel_lband_indicator'] = indicator_kc.keltner_channel_lband_indicator()
    
    #momentum
    res['rsi'] = ta.momentum.rsi(df["close"], window=14)
    res['ao'] = ta.momentum.awesome_oscillator(high=df["high"], low=df["low"], window1=5, window2=34) # 2 longest NaN
    res['tsi'] = ta.momentum.tsi(close=df["close"], window_slow=25, window_fast=13) # the longest NaN
    indicator_pvo = ta.momentum.PercentageVolumeOscillator(volume=df["volume"], window_slow=26, window_fast= 12, window_sign=9)
    res['pvo'] = indicator_pvo.pvo()
    res['pvo_signal'] = indicator_pvo.pvo_signal() # 2 longest NaN
    
    #trend
    indicator_macd = ta.trend.MACD(close=df["close"], window_slow = 26, window_fast = 12, window_sign = 9)
    res['macd'] = indicator_macd.macd()
    res['macd_signal'] = indicator_macd.macd_signal() # 2 longest NaN
    aroon_indicator = ta.trend.AroonIndicator(high=df["high"], low=df["low"], window=25)
    res['Aroon_down'] = aroon_indicator.aroon_down()
    res['Aroon_up'] = aroon_indicator.aroon_up()
    res['cci'] = ta.trend.cci(high=df["high"], low=df["low"], close=df["close"], window=20, constant=0.015)
    # late start - many Nan res['mass_index'] = ta.trend.mass_index(high=df["high"], low=df["low"], window_fast=9, window_slow=25)
    # late start - many Nan res['stc'] = ta.trend.stc(close=df["close"], window_slow=50, window_fast=23, cycle=10, smooth1=3, smooth2=3)
    res['wma'] = ta.trend.wma_indicator(close=df["close"], window=9)
    
    #volume
    indicator_easy_of_movement = ta.volume.EaseOfMovementIndicator(high=df["high"], low=df["low"], volume=df["volume"], window= 14)
    res['ease_of_movement'] = indicator_easy_of_movement.ease_of_movement()
    res['sma_ease_of_movement'] = indicator_easy_of_movement.sma_ease_of_movement()
    res['force_index'] = ta.volume.force_index(close=df["close"], volume=df["volume"], window=13)
    res['money_flow_index'] = ta.volume.money_flow_index(high=df["high"], low=df["low"], close=df["close"], volume=df["volume"], window=14)
    res['volume_weighted_average_price'] = ta.volume.volume_weighted_average_price(high=df["high"], low=df["low"], close=df["close"], volume=df["volume"], window=14)
    
    #target for the day `D` is the return between days `D+1` and `D+2`
    res['target'] = df['close'].pct_change(fill_method=None).shift(-2)

    return res

@ProgressdownDecorator(5, lambda x: x.name) # the function is used with pandas GroupBy.apply method, so the argument has the name attribute
def create_features(df: pd.DataFrame) -> pd.DataFrame:
    import warnings
    """
    Generate various technical indicators and features from the given DataFrame.
    Parameters:
    df (pd.DataFrame): DataFrame containing stock data with columns 'close', 'high', 'low', and 'volume'.
    Returns:
    pd.DataFrame: DataFrame containing the calculated technical indicators and features.
    Features:
    - Volatility:
        - Bollinger Bands (mavg, width, hband_indicator, lband_indicator)
        - Average True Range (atr)
        - Keltner Channel (mband, width, hband_indicator, lband_indicator)
    - Momentum:
        - Relative Strength Index (rsi)
        - Awesome Oscillator (ao)
        - True Strength Index (tsi)
        - Percentage Volume Oscillator (pvo, pvo_signal)
    - Trend:
        - Moving Average Convergence Divergence (macd, macd_signal)
        - Aroon Indicator (Aroon_down, Aroon_up)
        - Commodity Channel Index (cci)
        - Weighted Moving Average (wma)
    - Volume:
        - Ease of Movement (ease_of_movement, sma_ease_of_movement)
        - Force Index (force_index)
        - Money Flow Index (money_flow_index)
        - Volume Weighted Average Price (volume_weighted_average_price)
    - Target:
        - Return between days D+1 and D+2 (target)
    """
    res = pd.DataFrame(index=df.index)
    # chosen features
    # 'volatility_bbm', 'volatility_bbw', volatility_bbhi', 'volatility_bbli',
    # 'momentum_rsi', 'momentum_pvo', 
    # 'trend_macd', 'trend_dpo', 'trend_kst_diff', 'trend_adx',
    # 'trend_aroon_up', 'trend_aroon_down',
    # 'trend_psar_up_indicator', 'trend_psar_down_indicator', 
    # 'volume_adi', 'volume_cmf', 'volume_fi', 'volume_em', 'volume_sma_em',
    # 'volume_vpt', 'volume_nvi', 
    # 'others_dr', 'others_cr'- returns, they are target
    
    #volatility
    indicator_bb = ta.volatility.BollingerBands(close=df["close"], window=20, window_dev=2) # window=20, window_dev=2 - default
    res['Bollinger_mavg'] = indicator_bb.bollinger_mavg()
    res['Bollinger_width'] = indicator_bb.bollinger_wband()
    res['Bollinger_hband_indicator'] = indicator_bb.bollinger_hband_indicator()
    res['Bollinger_lband_indicator'] = indicator_bb.bollinger_lband_indicator()
    #volatility addition
    keltner_channel = ta.volatility.KeltnerChannel(high=df["high"], low=df["low"], close=df["close"], window=20, window_atr=10, original_version = True, multiplier = 2)
    res['keltner_channel_lband_indicator'] = keltner_channel.keltner_channel_lband_indicator()
    res['keltner_channel_hband_indicator'] = keltner_channel.keltner_channel_hband_indicator()
    res['keltner_channel_width'] = keltner_channel.keltner_channel_wband()
    res['ulcer_index'] = ta.volatility.ulcer_index(close=df["close"], window=14) 

    #momentum
    res['rsi'] = ta.momentum.rsi(df["close"], window=14)
    indicator_pvo = ta.momentum.PercentageVolumeOscillator(volume=df["volume"], window_slow=26, window_fast= 12, window_sign=9)
    res['pvo'] = indicator_pvo.pvo()
    
    #trend
    indicator_macd = ta.trend.MACD(close=df["close"], window_slow = 26, window_fast = 12, window_sign = 9)
    res['macd'] = indicator_macd.macd()
    res['dpo'] = ta.trend.dpo(close=df["close"], window=20)
    kst_indicator = ta.trend.KSTIndicator(close=df["close"], roc1=10, roc2=15, roc3=20, roc4=30, window1=10, window2=10, window3=10, window4=15, nsig=9)
    res['kst_diff'] = kst_indicator.kst_diff()
    #res['adx'] = ta.trend.adx(high=df["high"], low=df["low"], close=df["close"], window=14)
    aroon_indicator = ta.trend.AroonIndicator(high=df["high"], low=df["low"], window=25)
    res['Aroon_down'] = aroon_indicator.aroon_down()
    res['Aroon_up'] = aroon_indicator.aroon_up()
    #trend addition
    res['kst_sig'] = kst_indicator.kst_sig()
    res['Aroon_ind'] = aroon_indicator.aroon_indicator()
    res['cci'] = ta.trend.cci(high=df["high"], low=df["low"], close=df["close"], window=20, constant=0.015)
    
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', category=FutureWarning)
        psar_indicator = ta.trend.PSARIndicator(high=df["high"], low=df["low"], close=df["close"], step=0.02, max_step=0.2) 
        res['psar_down_indicator'] = psar_indicator.psar_down_indicator()
        res['psar_up_indicator'] = psar_indicator.psar_up_indicator()
    
    #volume
    indicator_easy_of_movement = ta.volume.EaseOfMovementIndicator(high=df["high"], low=df["low"], volume=df["volume"], window= 14)
    res['adi'] = ta.volume.acc_dist_index(high=df["high"], low=df["low"], close=df["close"], volume=df["volume"])
    res['cmf'] = ta.volume.chaikin_money_flow(high=df["high"], low=df["low"], close=df["close"], volume=df["volume"], window=20)
    res['force_index'] = ta.volume.force_index(close=df["close"], volume=df["volume"], window=13)
    res['ease_of_movement'] = indicator_easy_of_movement.ease_of_movement()
    res['sma_ease_of_movement'] = indicator_easy_of_movement.sma_ease_of_movement()
    res['volume_price_trend'] = ta.volume.volume_price_trend(close=df["close"], volume=df["volume"])
    res['nvi'] = ta.volume.negative_volume_index(close=df["close"], volume=df["volume"])
    #volume addition
    res['obv'] = ta.volume.on_balance_volume(close=df["close"], volume=df["volume"])

    #others
    res['day_return'] = ta.others.daily_return(df["close"])
    res['cumulative_return'] = ta.others.cumulative_return(df["close"])

    #target for the day `D` is the return between days `D+1` and `D+2`
    res['return'] = df['close'].pct_change(fill_method=None).shift(-2)

    return res

@ProgressdownDecorator(5, lambda x: x.name) # the function is used with pandas GroupBy.apply method, so the argument has the name attribute
def create_features_addition(df: pd.DataFrame) -> pd.DataFrame:
    
    res = pd.DataFrame(index=df.index)
    # chosen features
    # 'volatility_kcli', 'volatility_kchi', 'volatility_kcw',  'volatility_ui'
    # 'trend_kst_sig', 'trend_aroon_ind', , 'trend_cci'
    # 'volume_obv'
    
    #volatility
    keltner_channel = ta.volatility.KeltnerChannel(high=df["high"], low=df["low"], close=df["close"], window=20, window_atr=10, original_version = True, multiplier = 2)
    res['keltner_channel_lband_indicator'] = keltner_channel.keltner_channel_lband_indicator()
    res['keltner_channel_hband_indicator'] = keltner_channel.keltner_channel_hband_indicator()
    res['keltner_channel_width'] = keltner_channel.keltner_channel_wband()
    res['ulcer_index'] = ta.volatility.ulcer_index(close=df["close"], window=14) 

    #trend
    kst_indicator = ta.trend.KSTIndicator(close=df["close"], roc1=10, roc2=15, roc3=20, roc4=30, window1=10, window2=10, window3=10, window4=15, nsig=9)
    res['kst_sig'] = kst_indicator.kst_sig()

    aroon_indicator = ta.trend.AroonIndicator(high=df["high"], low=df["low"], window=25)
    res['Aroon_ind'] = aroon_indicator.aroon_indicator()
    res['cci'] = ta.trend.cci(high=df["high"], low=df["low"], close=df["close"], window=20, constant=0.015)
    #volume
    res['obv'] = ta.volume.on_balance_volume(close=df["close"], volume=df["volume"])

    return res