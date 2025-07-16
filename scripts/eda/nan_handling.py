import numpy as np
import pandas as pd

def edge_mean(row: pd.Series) -> float:
    if len(row)==2:
        return np.nan
    if len(row)!=3:
        raise ValueError('len(row) must be 2 or 3')
    center=1
    if pd.isna(row.iloc[center]) or row.iloc[center]==0:
        return np.mean([row.iloc[0], row.iloc[-1]])
    else:
        return row.iloc[center]
    
def reaplace_and_mark_nan_or_0(nan_value,repl_value,norm=None):
    if np.isnan(nan_value) or nan_value==0:
        res=[f'{round(repl_value,4)}*']
        if norm is not None:
            res.append(f'{round(repl_value/norm,4)}*')
    else:
        res=[nan_value]
        if norm is not None:
            res.append(nan_value/norm)
    return res    

def fillmark_nan_with_neighbors_mean(df_stocks_nan: pd.DataFrame, name_grouped: pd.api.typing.DataFrameGroupBy) -> pd.DataFrame: 
    """
    Fill NaN values in a DataFrame with the mean of 2 neighboring values within groups.

    This function fills NaN values in the 'open', 'high', 'low', 'close', and 'volume' columns of a DataFrame
    with the mean of the previous and next non-NaN values within the same group. If there are fewer than two
    neighbors, the NaN value remains. Additionally, it creates new columns showing the ratio of 'open', 'high',
    and 'low' prices to the 'close' price.

    :param df_stocks_nan (pd.DataFrame): DataFrame containing rows with NaN values.
    :param name_grouped (pd.api.typing.DataFrameGroupBy): Grouped DataFrame by 'Name' column.

    :return pd.DataFrame: DataFrame with NaN values filled and additional columns showing price ratios.
    """
    
    df_neighbors_means = pd.DataFrame(index=df_stocks_nan.index, columns=['open', 'open/close', 'high', 'high/close', 'low', 'low/close', 'close', 'volume'])

    for name,gr in name_grouped:
        mask = gr['open'].isna()
        # if there are nan in the group, print the mean of two neighbors for all nan values. If there is less than 2 neighbors, nan  will remain 
        if mask.sum()>0:
            mask3 = pd.concat([mask,mask.shift(-1), mask.shift(1)], axis=1).any(axis=1) # take neighbors for rows with nan
            neighbors_means = gr[mask3].rolling(window=3, center=True,min_periods=2).apply(edge_mean)
            neighbors_means = neighbors_means[mask[mask3]] # shrink mask to neighbors_means' size(mask[mask3]) and take rows by mask - where nan were 
            for (idx,row_nan), (_,row_repl) in zip(gr[mask].iterrows(), neighbors_means.iterrows()):
                df_neighbors_means.loc[idx,'close']=row_nan['close']
                for col_name in ['open', 'high', 'low']:
                    df_neighbors_means.loc[idx,[col_name, col_name+'/close']] = reaplace_and_mark_nan_or_0(row_nan[col_name],row_repl[col_name],row_nan["close"])
                df_neighbors_means.loc[idx,['volume']] = reaplace_and_mark_nan_or_0(row_nan['volume'],row_repl['volume'])

    return df_neighbors_means 


def zero2mean(s: pd.Series) -> pd.Series:
    """
    Replace zeros and NaNs in a pandas Series with the mean of their neighboring values.
    This function iterates through the Series and replaces any zero or NaN value with the mean 
    of its immediate non-zero and non-NaN neighbors. If the zero or NaN is at the beginning or 
    end of the Series, it is replaced with the nearest non-zero and non-NaN neighbor.

    :param  s (pd.Series): The input pandas Series containing numerical values.
    :return pd.Series: The modified pandas Series with zeros and NaNs replaced by the mean of their neighbors.
    """
    
    mask = (s==0) | s.isna() 
    indexes_of_zero = np.where(mask)[0].tolist()
    for idx in indexes_of_zero:
        if idx == 0 and s.iloc[idx + 1]!=0 and not np.isnan(s.iloc[idx + 1]):
            s.iloc[idx] = s.iloc[idx + 1]
        elif idx == len(s)-1 and s.iloc[idx - 1]!=0 and not np.isnan(s.iloc[idx - 1]):
            s.iloc[idx] = s.iloc[idx - 1]
        elif idx > 0 and idx < len(s)-1:
            s.iloc[idx] = np.int32(np.mean([s.iloc[idx - 1], s.iloc[idx + 1]]))
    return s  