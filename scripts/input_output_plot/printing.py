from typing import Any
from collections.abc import Iterable, Sequence

import pandas as pd

def output_formatting(data: Any, format: str) -> str:
    """
    add the format the data to prettify terminal output.
    :param data: any data which can be stringify
    :param color: string defining the format.
    It can be a number corresponding the ANSI escape code or a string composed of the code separate by `;`
    :return: string with added format before it and canceling all output formats after it
    """
    return f'\033[{format}m{data}\033[0m'


def print_info(df: pd.DataFrame, name: str):
        
    print(f'===infomation about {name} dataset===\n')
    print(df.info())
    print('-------------------------------------------------------------------')
    print(df.describe())
    print('-------------------------------------------------------------------')
    print('Unique values:\n')
    print(df.nunique())
    print('===================================================================\n')


def print_matrices(matrices: dict | Sequence, rows=2, cols=2):
    """
    Print a matrix of given matrices. 
    :param matrices: Sequence of matrices to print. 
    If the object has the method 'items()'(it is a pandas.Series or a dict) it will print the title of each matrix
    :param rows: number of rows in the output matrix of matrices
    (how many matrices to print in each row). Default is 2
    :param cols: number of columns in the output matrix of matrices
    (how many matrices to print in each column). Default is 2
    :return:
    """
    # Get the maximum number of rows among all matrices
    if hasattr(matrices, 'item'):
        matrices_tuples = list(matrices.items())
    else:
        matrices_tuples = [(f'matrix {i}',matrices[i]) for i in range(len(matrices))]
    for i in range(rows):
        current_matrices = matrices_tuples[i*cols:(i+1)*cols]
        title_str=' '
        max_rows = 0
        for title, matrix in current_matrices:
            title_str += ' ' + title + ' ' * (5 * len(matrix[0]) - len(title)) + '\t'
            max_rows = max(max_rows,len(matrix))

        print(title_str)
        for i in range(max_rows):
            # For each matrix, print the row if it exists, else print empty space
            for _, matrix in current_matrices:
                if i < len(matrix):
                    print(' '.join(f'{x:5.3}' for x in matrix[i]), end='\t')
                else:
                    print(' ' * 5 * len(' '.join(str(x) for x in matrix[0])), end='\t')
            print()
        print()


def DataFrames_to_matrix_str(dfs: dict | Sequence, cols=2):
    """
    returns a string disposing the matrix of given DataFarmes. The DataFrames must have the same indexes.
    :param dfs: iterable of matrices to print.
    If the object has the method 'items()'(it is a pandas.Series or a dict) it will print the title of each matrix
    :param cols: number of columns in the output matrix of matrices
    (how many matrices to print in each column). Default is 2
    :return:
    """
    item_size=4
    # Get the maximum number of rows among all matrices
    if hasattr(dfs, 'item'):
        matrices_tuples = list(dfs.items())
    else:
        matrices_tuples = [(f'matrix {i}', dfs[i]) for i in range(len(dfs))]
    rows_in_df = matrices_tuples[0][1].shape[0]
    indexes = matrices_tuples[0][1].index
    rows = len(dfs)//cols + 1
    res_str = ''
    for i in range(rows):
        current_matrices = matrices_tuples[i*cols:(i+1)*cols]
        tab_str = ' ' * (item_size+1)
        title_str = ''
        cols_str = ''
        line_str = ''
        for title, matrix in current_matrices:
            next_title = title + ' ' * ((item_size+1) * (len(matrix.columns)+1) - len(title))
            title_str += next_title + tab_str
            line_str += '-' * len(next_title) + tab_str
            cols_str += tab_str + ''.join(f'{str(col_name)[:item_size]:>5}' for col_name in matrix.columns) + tab_str
        res_str += title_str + '\n' + line_str + '\n' + cols_str + '\n'
        for i in range(rows_in_df):
            # For each matrix, print the row if it exists, else print empty space
            for _, matrix in current_matrices:
                res_str += f'{str(indexes[i])[:item_size]:>5}' + ''.join(f'{x:>5.3}' if isinstance(x,float) else f'{x:5}' for x in matrix.iloc[i]) + tab_str
            res_str += '\n'
        return res_str


def display_df_side_by_side(dfs, captions=None):
    from IPython.display import  display_html
    """
    Display multiple pandas DataFrames side by side in a Jupyter Notebook.

    :param dfs: List of DataFrames to display.
    :type dfs: list of pd.DataFrame
    :param captions: List of captions for each DataFrame. If None, default captions 'Table 1', 'Table 2', etc. will be used. The number of captions must match the number of DataFrames.
    :type captions: list of str, optional
    :raises ValueError: If the number of captions does not match the number of DataFrames.
    :return: This function displays the DataFrames side by side in the notebook.
    :rtype: None
    """
    if captions is None:
        captions = [f'Table {i}' for i in range(1, len(dfs)+1)]
    else:
        if len(captions) != len(dfs):
            raise ValueError('Number of titles should be equal to number of dataframes') 
    html_str=''
    for df,caption in zip(dfs, captions):
        html_str+=df.style.set_table_attributes("style='display:inline'").set_caption(caption)._repr_html_()
    display_html(html_str, raw=True)


def add_data_frames_to_file(path: str, dfs: dict, columns: Iterable|None = None):
    from tabulate import tabulate

    with open(path, 'a', encoding='utf-8') as f:
        for df_name, df in dfs.items():
            if columns is None:
                output_df = df
            else:
                output_df = df[columns]
            
            if isinstance(output_df.index, pd.MultiIndex):
                output_df = output_df.reset_index()

            print(f"Saving {df_name[:40]}...")
            f.write(f'\n### {df_name}\n')
            f.write(tabulate(output_df, headers='keys', tablefmt='pipe'))
            f.write('\n')
    print(f'--- data is saved to {path} ---')


def confusions_to_file(path: str, scores_dict: dict):
    """
    adds the confusion matrices from the dictionary of those into a file.
    :param path: the path to the file
    :param scores_dict:  a dictionary of confusion matrices,
    where a key is a name of a classifier and the value is a DataFrame of confusion matrices
    :return:
    """
    with open(path, 'a', encoding='utf-8') as f:
        for classificator_name, best_res in scores_dict.items():
            print(f'save confusion matrices for {classificator_name}...')
            f.write(f'\n{classificator_name}\n'+'*'*100 +'\n')
            f.write(DataFrames_to_matrix_str(best_res[['confusion_matrix', 'labels']].apply(lambda cfm: pd.DataFrame(cfm['confusion_matrix'],index=cfm['labels'], columns=cfm['labels']), axis=1), cols=4))
        print(f'--- confusion matrices are saved in {path} ---')

