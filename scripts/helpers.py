from collections import defaultdict
from collections.abc import Iterable
from functools import wraps
import time
from typing import Callable, Any

from consts import format
from input_output_plot.printing import output_formatting as paint

# import numpy as np
import pandas as pd


def is_iterable(obj: Any) -> bool: 
    return isinstance(obj, Iterable)


def list_or_none(obj: Iterable | None) -> bool:
    """"
    returns obj if obj is iterable, [] (an empty list) if obj is None, otherwise raises ValueError
    """
    if obj is None:
        return []
    elif is_iterable(obj):
        return obj
    else:
        raise ValueError('obj must be None or iterable')

    
def is_subdict(subdict: dict, dict: dict) -> bool:
    """
    Check if `subdict` is a subdictionary of `dict`.

    Args:
        subdict (dict): The dictionary to check if it is a subdictionary.
        dict (dict): The dictionary to check against.

    Returns:
        bool: True if `subdict` is a subdictionary of `dict`, False otherwise.
    """
    for key, val in subdict.items():
        try:
            if dict[key] != val:
                return False
        except KeyError:
            return False
    return True


def isnumber(number: str) -> bool:
    """
    Check if the given string represents a number.

    Args:
        number (str): The string to check.

    Returns:
        bool: True if the string represents a number, False otherwise.
    """
    try:
        float(number)
    except (ValueError, TypeError):
        return False
    else:
        return True


def timeit(func):
    """
        Decorator that times the execution of a function.

        This decorator wraps a function and times how long it takes to execute.
        It prints the execution time in seconds to the console and returns the result of the function,
        along with the total time taken.

        Args:
            func (callable): The function to time.

        Returns:
            tuple: A tuple containing the result of the function and the time taken to execute it.

        Usage:
            @timeit
            def my_func():
                ...
        """
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        #print(f'Function {func.__name__} took {total_time:.4f} seconds')
        return result, total_time
    return timeit_wrapper


class CountdownDecorator:
    """create a countdown decorator"""

    def __init__(self, num, callback=None):
        self.num = num
        self.callback = callback
        self.counter = num
        self.end_string = '... '
    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if self.counter == self.num:
                if self.callback is None:
                    print(f'run {args[0]}')
                else:
                    self.callback(*args, **kwargs)
            print(f'{self.counter}', end=self.end_string)
            result = func(*args, **kwargs)
            self.counter -= 1
            if self.counter <= 0:
                self.counter = self.num
                print('finished')
            return result
        return wrapper

class ProgressdownDecorator:
    """
    ProgressdownDecorator is a decorator class that provides a mechanism to print progress updates during the execution of a function.
    Attributes:
        step (int): The interval at which progress updates are printed.
        callback (callable, optional): A function to be called to generate the progress message. Defaults to None.
        counter (int): A counter to keep track of the number of function calls.
        progress_string (str): The string to print for each step that is not a progress update.
        end_string (str): The string to append at the end of each print statement.
    Methods:
        __call__(func):
            Wraps the given function to include progress updates.
        _print_progress_step(*args, **kwargs):
            Prints the progress update. If a callback is provided, it uses the callback's return value as the progress message.
    """

    def __init__(self, step, callback=None):
        self.step = step
        self.callback = callback
        self.counter = 0
        self.progress_string = '.'
        self.end_string = ''
    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if self.counter % self.step == 0:
                self._print_progress_step(*args, **kwargs)
            else:
                print(self.progress_string, end=self.end_string)
            self.counter += 1
            if self.counter % 100 == 0:
                print()
            result = func(*args, **kwargs)
            return result
        return wrapper
        
    def _print_progress_step(self, *args, **kwargs):
        if self.callback is None:
            print(f'step {self.counter}', end=self.end_string)
        else:
            print(f'{self.callback(*args, **kwargs)}', end=self.end_string)


def get_na_in_columns(df: pd.DataFrame, cols: list) -> pd.DataFrame:
    """
    Get all NaN values in columns.
    :param df: pandas DataFrame
    :param cols: Sequence of string, column names to search for NaN values
    :return: dataframe with rows from `df` which contains NaN values at least in one of `cols`
    """
    mask = df[cols].isna()
    return df[mask.any(axis=1)]


def find_first_diff(set1, set2):
    """
    Find the first differing element between two sequences.
    :param set1: First sequence
    :param set2: Second sequence
    :return: Index of the first differing element
    """
    counter = 0
    for s1, s2 in zip(set1, set2):
        if s1 != s2:
            break
        counter += 1
    return counter

def flatten_list_of_dicts(dicts):
    if isinstance(dicts, dict):
        return dicts
    else:
        flatten_param_grid = {}#defaultdict(list)
        for param_grid_elm in dicts:
            for key, value in param_grid_elm.items():
                if key not in flatten_param_grid:
                    flatten_param_grid[key] = value
                else:
                    for v in value:
                        if v not in flatten_param_grid[key]:
                            flatten_param_grid[key].append(v)
        return flatten_param_grid
    

def extract_capitals_with_following(s, n=3):
    """
    Extracts substrings from the input string `s` starting at each uppercase letter and including up to `n` characters
    or until the next uppercase letter is encountered.

    Args:
        s (str): The input string to process.
        n (int, optional): The number of characters to include after each uppercase letter. Defaults to 3.

    Returns:
        str: A concatenated string of the extracted substrings. If no uppercase letters are found, returns the original string.
    """
    result = []
    capitals =[]
    i = 0
    while i < len(s):
        if s[i].isupper():
            capitals.append(i)
        i += 1
    if len(capitals) == 0:
        return s
    capitals.append(len(s))
    for idx in range(len(capitals)-1):
        left=capitals[idx]
        right=min(left+n, capitals[idx+1])
        result.append(s[left:right])
    return ''.join(result)


def load_or_run(
    process: Callable[..., Any],
    file_path: str,
    *args,
    verbose: bool = True,
    **kwargs
) -> Any:
    
    from os.path import exists as path_exists
    from pickle import load as pkl_load, dump as pkl_dump
    def log(message: str):
        if verbose:
            print(message)

    if path_exists(file_path):
        log(f'Loading results from {paint(file_path, format)}')
        with open(file_path, 'rb') as f:
            return pkl_load(f)
    else:
        log(f'Running {process.__name__} and saving results to {paint(file_path, format)}')
        result = process(*args, **kwargs)
        with open(file_path, 'wb') as f:
            pkl_dump(result, f)
        return result