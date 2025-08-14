from typing import Iterable, Protocol
import warnings


import pandas as pd
from sklearn.base import BaseEstimator

from helpers import isnumber, is_iterable, is_subdict
from helpers import ProgressdownDecorator


def cv_scores(grid_search, par_names=None, score='score'):
    """
    Calculate cross-validation scores for specified parameters from a grid search.

    Parameters:
    grid_search (GridSearchCV): The grid search object containing the results of the cross-validation.
    par_names (str or list of str, optional): The parameter names for which to calculate the scores. 
                                              If None, scores for all parameters in best_params_ are calculated.
                                              If a string, calculates scores for the specified parameter.
                                              If a list of strings, calculates scores for each parameter in the list.
    score (str, optional): The score metric to use from the cv_results_. Default is 'score'.

    Returns:
    dict: A dictionary where keys are parameter names and values are the mean cross-validation scores for those parameters.

    Raises:
    ValueError: If par_names is not a string, list of strings, or None.
    """
    if par_names is None:
        par_names = grid_search.best_params_.keys()
    elif isinstance(par_names, str):
        return cv_scores_per_param(grid_search.best_params_, grid_search.cv_results_, par_names, score)
    elif is_iterable(par_names):
        pass
    else:
        raise (ValueError('par_names must be or string or a list of strings or None'))

    mean_scores = {}
    for par_name in par_names:
        mean_scores[par_name] = cv_scores_per_param(grid_search.best_params_, grid_search.cv_results_, par_name, score)
    return mean_scores


def cv_scores_per_param(best_params, cv_results, par_name, score='score'):
    """
    Extracts and returns cross-validation scores for a specific hyperparameter.

    This function filters the cross-validation results to find the scores 
    corresponding to a specific hyperparameter while keeping other parameters fixed.

    Parameters:
    -----------
    best_params : dict
        Dictionary containing the best parameters found during cross-validation.
    cv_results : dict
        Dictionary containing the cross-validation results, typically obtained from 
        a GridSearchCV or RandomizedSearchCV object.
    par_name : str
        The name of the hyperparameter for which the scores are to be extracted.
    score : str, optional
        The scoring metric used in cross-validation (default is 'score').

    Returns:
    --------
    mean_scores : pandas.DataFrame
        A DataFrame containing the mean training and testing scores for the specified 
        hyperparameter values. The index of the DataFrame corresponds to the hyperparameter values.
    """
    fixed = {key: val for key, val in best_params.items() if key != par_name}
    train_scores = []
    test_scores = []
    par_values = []
    for idx, candidate in enumerate(cv_results['params']):
        if is_subdict(fixed, candidate):
            try:
                if not isnumber(candidate[par_name]) and not isinstance(candidate[par_name], str):
                    par_value = str(candidate[par_name])
                else:
                    par_value = candidate[par_name]
                try:    
                    train_scores.append(cv_results[f'mean_train_{score}'][idx])
                except KeyError:
                    continue
                test_scores.append(cv_results[f'mean_test_{score}'][idx])
                par_values.append(par_value)
            except KeyError:
                continue
    if len(train_scores)>0:
        return pd.DataFrame({'train': train_scores, 'test': test_scores}, index=par_values)
    else:
        return pd.DataFrame({ 'test': test_scores}, index=par_values)


def cv_scores_per_params(grid_search, par_names, score='score'):
    """
    Extracts and returns cross-validation scores for specified parameters from a GridSearchCV object.
    Args:
        grid_search (GridSearchCV): The GridSearchCV object after fitting.
        params_names (list of str): List of parameter names to extract scores for.
        score (str, optional): The scoring metric to use. Defaults to 'score'.
    Returns:
        pd.DataFrame: A DataFrame with mean train and test scores for each combination of specified parameters.
    """

    import warnings
    best_params, cv_results = grid_search.best_params_, grid_search.cv_results_
    fixed = {key: val for key, val in best_params.items() if key not in par_names}

    sets = ['train', 'test']
    mean_scores = pd.DataFrame(index=pd.MultiIndex.from_product([[]]*len(par_names), names=par_names), columns=sets)

    with warnings.catch_warnings():
        for idx, candidate in enumerate(cv_results['params']):
            if is_subdict(fixed, candidate):
                par_values = _extract_parameter_values(par_names, candidate)
                for set_ in sets:
                    try:
                        mean_scores.loc[tuple(par_values), set_] = cv_results[f'mean_{set_}_{score}'][idx]
                    except KeyError:
                        continue
    return mean_scores

def _extract_parameter_values(params_names, candidate):
    par_values = []
    for par_name in params_names:
        try:
            if not isinstance(candidate[par_name], str) and  not isnumber(candidate[par_name]):
                par_values.append(str(candidate[par_name]))
            else:
                par_values.append(candidate[par_name])
        except KeyError:
            par_values.append('-')
            continue
    return par_values


def cv_scores_on_splits_per_param(grid_search, par_name, splits, scores='roc_auc'):
    import warnings

    if scores is None:
        scores = ['score']
    elif isinstance(scores, str):
        scores = [scores]
    elif not isinstance(scores, Iterable):
        raise ValueError("scores must be None or a string or an iterable object of strings")

    if splits is None:
        n_splits = grid_search.cv.get_n_splits()
        splits = list(range(n_splits))
    elif isinstance(splits, int):
        splits = [splits]
    elif not is_iterable(splits):
        raise ValueError('splits must be an integer or an iterable object of integers')
    
    if isinstance(grid_search.param_grid, dict):
        params_values = [str(val) for val in grid_search.param_grid[par_name]]
    else:
        params_values = []
        for param_grid_elm in grid_search.param_grid:
            try:
                params_values+=[str(val) for val in param_grid_elm[par_name]]
            except KeyError:
                continue

    
    best_params, cv_results = grid_search.best_params_, grid_search.cv_results_
    fixed = {key: val for key, val in best_params.items() if key != par_name}
    splits_names = [f'split{i:d}' for i in splits]
    sets = ['train', 'test']
    scores_matrix = pd.DataFrame(index=pd.MultiIndex.from_product([splits_names, sets], names=['split', 'set']), 
                                 columns=pd.MultiIndex.from_product([params_values, scores], names=['param_value', 'score']))
    
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', category=pd.errors.PerformanceWarning) 
        for idx, candidate in enumerate(cv_results['params']):
            if is_subdict(fixed, candidate):
                par_value = _extract_parameter_values([par_name], candidate)[0]
                for set_ in sets:
                    for split in splits_names:
                        for score in scores:
                            try:
                                scores_matrix.loc[(split, set_), (par_value, score)] = cv_results[f'{split}_{set_}_{score}'][idx]
                            except KeyError:
                                continue
    scores_matrix = scores_matrix.astype(float)\
        .sort_index(level='split', key=lambda x: x.map(lambda x: int(x.split('split')[-1])), sort_remaining=True)\
        .sort_index(axis=1, level='param_value', sort_remaining=True)
        
    return scores_matrix


def cv_scores_on_splits(grid_search, n=3, scores:Iterable|str|None=None, confusion_matrix_cells: Iterable|None=None):
    """
    Calculate cross-validation scores on splits for a given grid search object.
    Parameters:
    -----------
    grid_search : GridSearchCV
        The grid search object containing the cross-validation results.
    n : int, optional (default=3)
        The number of top scores to extract.
    scores : Iterable, str, or None, optional (default=None)
        The scores to extract. If None, defaults to ['score']. If a string is provided, it will be converted to a list containing that string.
    confusion_matrix_cells : Iterable or None, optional (default=None)
        The confusion matrix's cells names used in the scores. If None, defaults to an empty list.
    Returns:
    --------
    top_scores_matrix : pd.DataFrame
        A DataFrame containing the top scores for each split and set (train/test).
    """

    import warnings
    from collections.abc import Iterable

    if scores is None:
        scores = ['score']
    elif isinstance(scores, str):
        scores = [scores]
    elif not isinstance(scores, Iterable):
        raise ValueError("scores must be None or a string or an iterable object of strings")
    
    if confusion_matrix_cells is None:
        confusion_matrix_cells = []
    elif not isinstance(confusion_matrix_cells, Iterable):
        raise ValueError("confusion_matrix_cells must be None or an iterable object of strings")
    
    # name = grid_search.estimator.__class__.__name__
    # if name == 'Pipeline':
    #     name = grid_search.estimator.steps[-1][0]

    cv_results = grid_search.cv_results_
    n_splits = grid_search.cv.get_n_splits()
    if isinstance(grid_search.param_grid, dict):
        params_names = grid_search.param_grid.keys()
    else:
        params_names = {name_ for param_grid_elm in grid_search.param_grid for name_ in param_grid_elm.keys()}
    
    column_names = [param_name.split('__')[-1] for param_name in params_names]

    splits = [f'split{i:d}' for i in range(n_splits)]
    sets = ['train', 'test']

    top_scores_matrix = pd.DataFrame(index=pd.MultiIndex.from_product([splits, sets, *[[]]*len(params_names)], names=['split', 'set', *column_names]), columns=[*scores, *confusion_matrix_cells])
    best_estimator_scores = pd.DataFrame(index=pd.MultiIndex.from_product([splits, sets], names=['split', 'set']), columns=[*scores, *confusion_matrix_cells])

    with warnings.catch_warnings():
        warnings.simplefilter('ignore', category=pd.errors.PerformanceWarning) 
        for split in splits:
            for set_ in sets:
                for score in scores:
                    try:
                        fit_scores = cv_results[f'{split}_{set_}_{score}'] # scores for all candidates
                    except KeyError:
                        continue
                    _extract_top_fit_scores(top_scores_matrix, n, cv_results, fit_scores, params_names, confusion_matrix_cells, score, split, set_)
                    best_estimator_scores.loc[(split, set_), score] = fit_scores[grid_search.best_index_]
                for cm_cell in confusion_matrix_cells:
                    best_estimator_scores.loc[(split, set_), cm_cell] = cv_results[f'{split}_{set_}_{cm_cell}'][grid_search.best_index_]
                

    top_scores_matrix = top_scores_matrix.astype(float).sort_index(level='split', key=lambda x: x.map(lambda x: int(x.split('split')[-1])), sort_remaining=True)
    best_estimator_scores = best_estimator_scores.astype(float)
    return top_scores_matrix, best_estimator_scores

def _extract_top_fit_scores(res, n, cv_results, fit_scores, params_names, confusion_matrix_cells, score, split, set_):
    import heapq
    fits_params = cv_results['params']
    n_fits =  len(fits_params)
    if n is None:
        largest_indexes = range(n_fits)
    else:
        largest_indexes = heapq.nlargest(n, range(n_fits), key=fit_scores.__getitem__)
    for idx in largest_indexes:
        fit_params_values = []
        for param_name in params_names:
            try:
                fit_params_values.append(str(fits_params[idx][param_name]))
            except KeyError:
                fit_params_values.append('-')
        res.loc[(split, set_, *fit_params_values), score] = fit_scores[idx]
        for cm_cell in confusion_matrix_cells:
            res.loc[(split, set_, *fit_params_values), cm_cell] = cv_results[f'{split}_{set_}_{cm_cell}'][idx]


def create_comparation_table(stages_grid_search_results, stages_names, models_to_compare, params_to_compare):
    from helpers import extract_capitals_with_following
    comparation_df = pd.DataFrame(
        index=pd.MultiIndex.from_product([models_to_compare, params_to_compare], names=['model', 'param']),
        columns=stages_names#['presecelecting', 'scaler-reducer', 'scaler-reducer2', 'train_len', 'diff sr2-len']
    )
    def compare_row(row):
        if 'score' in row.name:
            return f'Best: {row.idxmax()}'
        elif row.nunique(dropna=False) == 1:
            return 'Same'
        else:
            return '--'
    
    for stage_name, grid_search_results in zip(stages_names, stages_grid_search_results):
        results_by_name = {res['name']: res['key_results'] for res in grid_search_results if res['name'] in models_to_compare}
            
        for model_name in models_to_compare:
            key_res = results_by_name[model_name]
            if 'score' in params_to_compare:
                comparation_df.loc[(model_name, 'score'), stage_name] = key_res['Best scores']
            for param_name in params_to_compare:
                if param_name != 'score' and param_name in key_res['Best parameters']:
                    comparation_df.loc[(model_name, param_name), stage_name] = extract_capitals_with_following(str(key_res['Best parameters'][param_name]))
            #  params
            for k, v in key_res['Best parameters'].items():
                if model_name in k:
                    par_name = k.split('__')[-1]
                    comparation_df.loc[(model_name, f'{par_name}_best'), stage_name] = str(v)
                    comparation_df.loc[(model_name, f'{par_name}_grid'), stage_name] = str(key_res['Parameters grid'][k])

    comparation_df['diff'] = comparation_df.apply(compare_row, axis=1)
    
    return comparation_df.sort_index()


def _is_best_param_grid(best_params, param_grid):
    for k,v in best_params.items():    
        try:
            if v not in param_grid[k]:
                return False
        except KeyError:
            return False
    return True

def cv_scores_on_splits_by_param(grid_search, param_name:str, score:str='roc_auc',):
    import warnings

    n_splits = grid_search.cv.get_n_splits()
    best_params = grid_search.best_params_
    cv_results = grid_search.cv_results_
    if isinstance(grid_search.param_grid, dict):
        param_grid = grid_search.param_grid[param_name]
    else:
        for param_grid_elm in grid_search.param_grid:
            if _is_best_param_grid(best_params, param_grid_elm):
                param_grid = param_grid_elm[param_name]
                break
                    
    fixed = {key: val for key, val in best_params.items() if key != param_name}

    splits = [f'split{i:d}' for i in range(n_splits)]
    sets = ['train', 'test']
    score_matrix = pd.DataFrame(index=pd.MultiIndex.from_product([splits, sets], names=['split', 'set']), columns=param_grid)

    with warnings.catch_warnings():
        for idx, candidate in enumerate(cv_results['params']):
            if is_subdict(fixed, candidate):
                for split in splits:
                    for set_ in sets:
                        try:
                            score_matrix.loc[(split, set_), candidate[param_name]] = cv_results[f'{split}_{set_}_{score}'][idx]
                        except KeyError:
                            continue

    return score_matrix


class Cv_splitter(Protocol):
    def split(self, X): ...

def custom_warning_handler(ws, shown_warnings):
        for w in ws:
            w_id = w.filename+':'+str(w.lineno)
            if w_id not in shown_warnings:
                shown_warnings.add(w_id)
                print(f"\nWarning: {w_id}: {w.category.__name__}: {w.message}")
                
def compare_scores_on_splits(model_tuples:tuple[str,BaseEstimator]|list[tuple[str,BaseEstimator]],
                             cv:Cv_splitter,
                             X:pd.DataFrame,
                             y:pd.Series,
                             score_names:str|list[str]=['accuracy', 'roc_auc'],
                             verbose=True) -> pd.DataFrame: 
    """
    Evaluates multiple machine learning models across different data splits using cross-validation.

    Parameters:
    ----------
    model_tuples : tuple or list of tuples
        A tuple or list of tuples where each tuple contains a model name (str) and the corresponding estimator (BaseEstimator).
    
    cv : Cv_splitter, optional
        Cross-validation splitter instance that defines the train-test split strategy (default is tscv_blocking_chosen).
    
    score_names : str or list of str, optional
        A string or list of strings specifying the evaluation metrics to compute (default: ['accuracy', 'roc_auc', 'f1']).
    
    X : pd.DataFrame, optional
        Feature dataset used for model evaluation (default: X_train).
    
    y : pd.Series, optional
        Target values corresponding to X (default: y_train).

    Returns:
    -------
    scores : pd.DataFrame
        A DataFrame containing model performance scores across splits.
        Columns are a MultiIndex of model names and score metrics, indexed by split number.

    Notes:
    ------
    - Models are fitted on the training indices provided by the cross-validation splitter.
    - Scores are calculated for each test split using a predefined scoring function.

    Example:
    --------
    >>> models = [('RandomForest', RandomForestClassifier()), ('LogisticRegression', LogisticRegression())]
    >>> cv = TimeSeriesSplit(n_splits=5)
    >>> compare_scores_on_splits(models, cv, ['accuracy', 'f1'], X_train, y_train)
    """
    from sklearn.metrics import get_scorer

    if isinstance(score_names, str) :
        score_names = [score_names]

    if not isinstance(model_tuples, list):
        model_tuples = [model_tuples]
    
    model_names = [model_tuple[0] if isinstance(model_tuple, tuple) else str(model_tuple) for model_tuple in model_tuples ]
    
    if verbose:
        print(f'Comparing scores on splits with {len(model_tuples)} models: \"{"\", \"".join(model_names)}\".')
        progressdown_decorator = ProgressdownDecorator(len(model_tuples), lambda model, X, y: f'\nfit the models on {len(X)} samples .')
    else:
        progressdown_decorator = lambda f: f
    
    @progressdown_decorator
    def fit(model, X, y): model.fit(X, y) 
    
    scores = pd.DataFrame(columns=pd.MultiIndex.from_product([model_names, score_names]), index=pd.Index(range(11), name='splits'))
    scorers = {score_name: get_scorer(score_name) for score_name in score_names}
    i = 0
    shown_warnings = set()
    for tr_idx, ts_idx in cv.split(X):
        for model_name, model in model_tuples:
            with warnings.catch_warnings(record=True) as w:
                fit(model, X.iloc[tr_idx], y.iloc[tr_idx])
                custom_warning_handler(w, shown_warnings)

            for score_name in score_names:
                scores.loc[i, (model_name, score_name)] = scorers[score_name](model, X.iloc[ts_idx], y.iloc[ts_idx])
        i += 1
    return scores

def predictions_on_splits(models:list[BaseEstimator]|BaseEstimator, 
                          cv:Cv_splitter,
                          X:pd.DataFrame,
                          y:pd.Series,
                          verbose=True)->dict[list, list]:
    
    if isinstance(models, BaseEstimator):
        models = [models]
    num_models = len(models)

    predictions_proba = [[] for _ in range(num_models)]
    predictions = [[] for _ in range(num_models)]
    predicted_probabilities = []
    predicted = [] 

    if verbose:
        print(f'Predicting on splits with {num_models} models.')
        progressdown_decorator = ProgressdownDecorator(num_models, lambda model, X, y, split_num: f'\nSplit {split_num+1}: fit and predict on the models on {len(X)} samples .')
    else:
        progressdown_decorator = lambda f: f
    
    @progressdown_decorator
    def fit(model, X, y, split_num): model.fit(X, y) 

    shown_warnings = set()
    for split_num, (train_index, test_index) in enumerate(cv.split(X)):
        X_train_fold, X_val_fold = X.iloc[train_index], X.iloc[test_index]
        y_train_fold, y_val_fold = y.iloc[train_index], y.iloc[test_index]
        for i, model in enumerate(models):
            with warnings.catch_warnings(record=True) as w:
                fit(model, X_train_fold, y_train_fold, split_num)
                custom_warning_handler(w, shown_warnings)
    
            res = model.predict_proba(X_val_fold)
            predictions_proba[i].append(pd.Series(res[:, 1], index=X_val_fold.index))
            res = model.predict(X_val_fold)
            predictions[i].append(pd.Series(res, index=X_val_fold.index))


    for i in range(num_models):
        predicted_probabilities.append(pd.concat(predictions_proba[i]))
        predicted.append(pd.concat(predictions[i]))
    return {
        'predicted_probabilities': predicted_probabilities,
        'predicted': predicted,
    }
