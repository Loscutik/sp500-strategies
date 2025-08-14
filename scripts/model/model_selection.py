from os.path import isfile as path_isfile
from pickle import load as pkl_load, dump as pkl_dump
from typing import Protocol, Iterable

import pandas as pd

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import TargetEncoder
from sklearn.model_selection import TimeSeriesSplit
from sklearn.pipeline import Pipeline

from consts import format
from input_output_plot.printing import output_formatting as paint
from model.estimating import WrapModelTrainSizeParam, run_classifier_grid_search


class MultiTimeSeriesSplit(TimeSeriesSplit):  
    """MultiTimeSeriesSplit is a custom cross-validator for time series data that allows for multiple splits with varying train and test sizes.
    
    Parameters
    ----------
    n_splits : int, default=5
        Number of splits. Must be at least 2.
    min_train_size : int, default=1
        Minimum size of the training set.
    max_train_size : int, optional
        Maximum size of the training set. If None, the training set size is not limited.
    test_size : int, optional
        Size of the test set. If None, it will be calculated based on the number of splits and the gap.
    gap : int, default=0
        Number of observations to exclude from the end of each train set before the test set.
    
    Attributes
    ----------
    test_ranges : list of tuples
        List of tuples containing the start and end dates for each test set.
    test_range_lengths : list of int
        List of lengths of each test set.
    
    Methods
    -------
    get_n_splits(X=None, y=None, groups=None)
        Returns the number of splits.
    get_test_size()
        Returns the size of the test set.
    get_test_ranges()
        Returns the list of test ranges.
    get_test_ranges_len()
        Returns the list of test range lengths.
    split(X, y=None, groups=None)
        Generates indices to split data into training and test set.
    Raises
    ------
    ValueError
        If the test size is less than or equal to 0, or if the number of splits is too many for the given number of dates, minimum train size, and gap."""
    
    def __init__(self, n_splits=5, *, min_train_size=1, max_train_size=None, test_size=None, gap=0):  
        self.n_splits = n_splits
        self.min_train_size = min_train_size
        self.max_train_size = max_train_size
        self.test_size = test_size
        self.gap = gap
        self.test_ranges = None
        self.test_range_lengths = None
    
    def get_n_splits(self, X=None, y=None, groups=None):  
        return self.n_splits  
    
    def get_test_size(self):
        return self.test_size
    
    def get_test_ranges(self):
        return self.test_ranges
    
    def get_test_ranges_len(self):
        return self.test_range_lengths
    
    def get_min_train_size(self):
        return self.min_train_size
    
    def get_params(self, deep=True):
        return {
            'n_splits': self.n_splits,
            'min_train_size': self.min_train_size,
            'max_train_size': self.max_train_size,
            'test_size': self.test_size,
            'gap': self.gap
        }
    
    def __validate_test_size(self, n_dates, test_size):
        if test_size <= 0:
            raise ValueError(
                f"Too many splits={self.n_splits} for number of dates={n_dates} "
                f"with min_train_size={self.min_train_size} and gap={self.gap}."
            )
        
    def split(self, X, y=None, groups=None):  
        """
        Split the DataFrame X indexed by date. Index must have a level 'date'. 
        """
        dates = X.index.get_level_values('date').unique().sort_values()
        n_dates = dates.size
        
        if self.test_size is None:
            test_size = (n_dates - self.gap)//(self.n_splits+1)
            self.__validate_test_size(n_dates, test_size)

            if n_dates - self.gap - test_size * self.n_splits < self.min_train_size:
                test_size = (n_dates - self.gap - self.min_train_size)//self.n_splits
                self.__validate_test_size(n_dates, test_size)
            self.test_size = test_size    
        else:
            test_size = self.test_size
            self.__validate_test_size(n_dates, test_size)
            if n_dates - self.gap - self.min_train_size - test_size * self.n_splits<0:
                raise ValueError(
                    f"Too many splits={self.n_splits} for number of dates {n_dates}="
                    f"with min_train_size={self.min_train_size}, {test_size=} and gap={self.gap}."
                )

        test_starts = range(n_dates - test_size * self.n_splits, n_dates, test_size)
        # let get date ranges for each test set
        self.test_ranges = [(dates[test_start], dates[min(len(dates)-1, test_start + test_size - 1)]) for test_start in test_starts]
        self.test_range_lengths = [len(dates[test_start:test_start+test_size]) for test_start in test_starts]
        for test_start in test_starts:
            train_end = test_start - self.gap
            if self.max_train_size is not None and self.max_train_size < train_end:
                train_dates = dates[train_end - self.max_train_size : train_end]
                test_dates = dates[test_start : test_start + test_size]
                yield (
                    X.index.get_indexer_for(train_dates),
                    X.index.get_indexer_for(test_dates),
                )
            else:
                train_dates = dates[:train_end]
                test_dates = dates[test_start : test_start + test_size]
                yield (
                    X.index.get_indexer_for(train_dates),
                    X.index.get_indexer_for(test_dates),
                )


def is_train_test_folds_have_common_dates(cv: TimeSeriesSplit, X: pd.DataFrame) -> bool:
    """
    Check if there are any overlapping dates between the train and test folds
    produced by a cross-validation splitter.

    Args:
        cv: Cross-validation splitter object with a split method.
        X: DataFrame with a DatetimeIndex or MultiIndex including dates.

    Returns:
        bool: True if any train and test fold share at least one date, False otherwise.
    """
    for tr, tt in cv.split(X=X):
        tr_dates = X.iloc[tr].index.unique()
        tt_dates = X.iloc[tt].index.unique()
        if tr_dates.intersection(tt_dates).size>0:
            return True
    return False


def make_pipeline(configed_model, column_transformers, configed_dim_reducers=None, train_set_lengths=None):
    """
        Creates a pipline for a model which consists of
        - a column transformer layer
        - a model layer, which is a model wrapped by WrapTrainSizeParam class. WrapTrainSizeParam adds the size of train set to the model's parameters.
    """
    # TODO add support for transformers parameters, like for dim_redusers; use itertools.product to simplify the code
    STEP_NAME_REDUCER = "reduce_dim"
    STEP_NAME_TRANSFORMER = "transformer"

    params = configed_model['params']
    model_name = configed_model['model'].__name__.lower()

    param_grid =  {f"{model_name}__{param_name}": param_values  for param_name, param_values in params.items()}
    if train_set_lengths is not None:
        param_grid[f"{model_name}__train_length"] = train_set_lengths
        model = WrapModelTrainSizeParam(configed_model['model'])
    else:
        model = configed_model['model']()
    
    if isinstance(column_transformers, list) or isinstance(column_transformers, tuple):
        transformer = "passthrough"
        param_grid[STEP_NAME_TRANSFORMER] = column_transformers
    else:
        transformer = column_transformers

    if configed_dim_reducers is None:
        reducer_dim = "passthrough"
    elif isinstance(configed_dim_reducers, list) or isinstance(configed_dim_reducers, tuple):
        reducer_dim = "passthrough"
        param_grid_exemplar = param_grid
        param_grid = []
        for configed_reducer in configed_dim_reducers:
            r_params = configed_reducer['params']
            r_model = configed_reducer['model']
            param_grid_current = param_grid_exemplar.copy()
            param_grid_current[STEP_NAME_REDUCER] = [r_model]
            for param_name, param_values in r_params.items():
                param_grid_current[f"{STEP_NAME_REDUCER}__{param_name}"] = param_values
            param_grid.append(param_grid_current)
    else:
        reducer_dim = configed_dim_reducers['model']
        for param_name, param_values in configed_dim_reducers['params'].items():
            param_grid[f"{STEP_NAME_REDUCER}__{param_name}"] = param_values

    pipeline = Pipeline([
        (STEP_NAME_TRANSFORMER, transformer),
        (STEP_NAME_REDUCER, reducer_dim), 
        (model_name, model)
        ])
    return {
        'model': pipeline,
        'params':param_grid,
        }


def train_classifiers(results_file, classifiers, X, y, scoring, cv, column_transformers, configed_dim_reducers=None, train_set_lengths=None, return_train_score=True, refit='roc_auc',**kwargs):
    """
    runs grid search on chosen classifiers and reruns a dictionary with results:  

    {  
        'search_time': execution time in sec,  
        'grid_search': fitted GridSearchCV object,  
    }
"""
    
    grid_search_results = []
    models_names = [configed_model['model'].__name__.lower() for configed_model in classifiers]
    def are_keys_in_list(keys, list_):
        for key in keys:
            if key not in list_:
                return False
        return True
    
    if not isinstance(column_transformers, dict) or not are_keys_in_list(models_names, column_transformers.keys()):
        column_transformers = {configed_model['model'].__name__.lower() : column_transformers for configed_model in classifiers}
    if not isinstance(configed_dim_reducers, dict) or not are_keys_in_list(models_names, configed_dim_reducers.keys()):
        configed_dim_reducers = {configed_model['model'].__name__.lower() : configed_dim_reducers for configed_model in classifiers}


    if not path_isfile(results_file):
        for configed_model in classifiers:
            model_name = configed_model['model'].__name__.lower()
            print(f'Run grid search on {paint(model_name, format)} classifier')
            print('With', paint('parameters:',format), configed_model['params'])
            print('For', paint('train set lengths:', format), train_set_lengths)
            pipeline = make_pipeline(configed_model, column_transformers[model_name], configed_dim_reducers[model_name], train_set_lengths)
            #print('Pipeline:', pipeline)
            grid_search_result = run_classifier_grid_search( 
                pipeline,
                X, y,
                scoring=scoring,
                refit=refit,
                cv=cv,
                return_train_score=return_train_score,
                **kwargs
            )
            grid_search_result['name'] = model_name
            grid_search_results.append(grid_search_result)
        
            print('-----------------------------------------------------')
            print(f"Grid search took {paint(grid_search_result['search_time']/60, format)} minutes")
            print(paint('Best parameters:',format), grid_search_result['grid_search'].best_params_)
            print(paint('Best scores:',format), grid_search_result['grid_search'].best_score_)
            print('===================================================================================================================')
        
        with open(results_file, 'wb') as f:
            pkl_dump(grid_search_results, f)
    else:
        print(f'load trained models from {results_file}')
        with open(results_file, 'rb') as f:
            grid_search_results = pkl_load(f)
        for grid_search_result in grid_search_results:
            print(f"Model {paint(grid_search_result['name'], format)}:")
            print('With', paint('parameters:',format), grid_search_result['grid_search'].param_grid)
            print(f"\nBest parameters: {paint(grid_search_result['grid_search'].best_params_, format)}")
            print(f"Best scores: {paint(grid_search_result['grid_search'].best_score_, format)}")
            print(f"Search time: {paint(grid_search_result['search_time']/60, format)} minutes")
            print('===================================================================================================================')

    return grid_search_results


class Transformer(Protocol):
    def fit(self, X, y=None): ...
    def transform(self, X): ...
    def fit_transform(self, X, y=None): ...


class EncoderNameScalerDigitCols(ColumnTransformer):
    """
    A custom ColumnTransformer that applies a specified encoder to a set of columns (typically categorical),
    and optionally applies additional transformers to other columns.

    Parameters
    ----------
    encoder_columns : list of str
        List of column names to which the encoder will be applied.
    encoder : Transformer or str, default=TargetEncoder(cv=5)
        The encoder to apply to encoder_columns. Can be a transformer instance or 'passthrough'.
    transformers_columns : Iterable of tuples (Transformer, list of str), optional
        List of (transformer, columns) pairs specifying additional transformers and their target columns.
    remainder : Transformer or str, default='passthrough'
        Transformer for columns not specified in encoder_columns or transformers_columns.
    verbose_feature_names_out : bool, default=True
        Whether to include transformer names as prefixes in output feature names.

    Methods
    -------
    get_params(deep=True)
        Get parameters for this transformer.
    set_params(**params)
        Set the parameters of this transformer.
    _make_transformer_tuples()
        Internal method to construct the list of transformer tuples for ColumnTransformer.
    """
    def __init__(self, 
                 encoder_columns:list[str],
                 encoder:Transformer|str=TargetEncoder(cv=5), 
                 transformers_columns:Iterable[tuple[Transformer, list[str]]]=None, 
                 remainder:Transformer|str='passthrough',
                 verbose_feature_names_out:bool=True):  
        # transformers_columns is a list of tuples (transformer, columns) specifying the transformer objects to be applied to the columns 
        self.transformers_columns = transformers_columns
        self.encoder_columns = encoder_columns
        self.encoder = encoder
        self.remainder = remainder
        self.verbose_feature_names_out=verbose_feature_names_out
        transformer_sequence = self._make_transformer_tuples()
        super().__init__(transformers=transformer_sequence, remainder=self.remainder, verbose_feature_names_out=self.verbose_feature_names_out)  
        # self.set_output(transform='pandas')
  
    def get_params(self, deep=True):  
        params = super().get_params(deep=deep)
        params['transformers_columns'] = self.transformers_columns 
        params['encoder_columns'] = self.encoder_columns
        params['encoder'] = self.encoder
        params['remainder'] = self.remainder
        return params  
  
    def set_params(self, **params):
        self.transformers_columns = params.pop('transformers_columns',self.transformers_columns)
        self.encoder_columns = params.pop('encoder_columns',self.encoder_columns)
        self.encoder = params.pop('encoder',self.encoder) 
        self.verbose_feature_names_out = params.pop('verbose_feature_names_out', self.verbose_feature_names_out)
        print('set',self.transformers_columns)
        transformer_sequence = self._make_transformer_tuples()
        encoder_columns = self.encoder_columns
        encoder = self.encoder
        verbose_feature_names_out = self.verbose_feature_names_out
        self = ColumnTransformer(transformers=transformer_sequence, remainder=self.remainder, verbose_feature_names_out=self.verbose_feature_names_out)  
        self.encoder_columns = encoder_columns
        self.encoder = encoder
        self.verbose_feature_names_out = verbose_feature_names_out
        super().set_params(**params)
        return self
  
    def _make_transformer_tuples(self):
        #(name, transformer, columns) 
        if self.transformers_columns is None or self.transformers_columns == 'passthrough':
            self.transformers_tuples = [] 
        else:
            self.transformers_tuples = [(transformer.__class__.__name__, transformer, transformer_columns) for transformer, transformer_columns in self.transformers_columns]   
        
        return [
            ('name_encoder', self.encoder, self.encoder_columns),
            *self.transformers_tuples, 
        ]
    

class NamedTransformer(BaseEstimator, TransformerMixin):
    """
    A wrapper for scikit-learn transformers that assigns a custom name for identification.

    Parameters
    ----------
    transformer : TransformerMixin
        The transformer instance to wrap.
    name : str
        The custom name to assign to this transformer.

    Methods
    -------
    fit(X, y=None)
        Fit the wrapped transformer.
    transform(X)
        Transform the data using the wrapped transformer.
    __repr__()
        Return the custom name as the string representation.
    describe()
        Return the string representation of the transformer.
    get_feature_names_out()
        Get output feature names from the wrapped transformer.
    """
    def __init__(self, transformer, name):
        self.transformer = transformer
        self.name = name
    def fit(self, X, y=None):
        return self.transformer.fit(X, y)
    def transform(self, X):
        return self.transformer.transform(X)
    def __repr__(self):
        return self.name
    def describe(self):
        return self.__str__()
    def get_feature_names_out(self):
        return self.transformer.get_feature_names_out()