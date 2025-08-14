import pandas as pd

from model.validating import cv_scores_on_splits, cv_scores, cv_scores_per_params, create_comparation_table, cv_scores_on_splits_by_param, cv_scores_on_splits_per_param
from input_output_plot.printing import add_data_frames_to_file

from consts import format
from input_output_plot.printing import output_formatting as paint
from input_output_plot.plotting import lineplot
from helpers import flatten_list_of_dicts

KEY_BEST_ESTIMATOR_SCORES = 'best_estimator_scores'

def create_tables_of_best_scores(grid_search_results:list[dict], 
                                 scores=['accuracy', 'average_precision', 'f1', 'roc_auc', 'log_loss'], 
                                 confusion_matrix_cells=['tn', 'fp', 'fn', 'tp']):
    for grid_search_result in grid_search_results:
        print(grid_search_result['name'])
        grid_search_result['scores_on_splits'], grid_search_result[KEY_BEST_ESTIMATOR_SCORES] = \
            cv_scores_on_splits(grid_search_result['grid_search'], scores=scores, confusion_matrix_cells=confusion_matrix_cells, n=2)


def add_scores_of_stage_to_file(grid_search_results:list[dict], 
                                 stage:str, 
                                 file_path:str,
                                 scores=['accuracy', 'average_precision', 'f1', 'roc_auc', 'log_loss'], 
                                 confusion_matrix_cells=['tn', 'fp', 'fn', 'tp']):
    create_tables_of_best_scores(grid_search_results, scores=scores, confusion_matrix_cells=confusion_matrix_cells)
    with open(file_path, 'a', encoding='utf-8') as f: 
        f.write(f'\n\n## Stage: {stage} \n')
    scores_dfs = {f"{grid_search_result['name']}\n({grid_search_result['grid_search'].best_params_})\ntime: {grid_search_result['search_time']/60} min\n":
              grid_search_result[KEY_BEST_ESTIMATOR_SCORES] for grid_search_result in grid_search_results}
    add_data_frames_to_file(file_path, scores_dfs)

    
def add_grid_search_key_results(grid_search_results:list[dict], stage:str, file_path:str):
    """
    Save key results of grid search to a markdown file.
    Each grid search result will be saved with its parameters, best parameters, best score, and search time.
    """
    with open(file_path, 'a', encoding='utf-8') as f: 
        f.write(f'\n\n## Stage: {stage} \n')
        for grid_search_result in grid_search_results:
            param_grid = flatten_list_of_dicts(grid_search_result["grid_search"].param_grid)
             
            grid_search_result['key_results'] = pd.Series([
                param_grid, 
                grid_search_result["grid_search"].best_params_, 
                grid_search_result["grid_search"].best_score_, 
                grid_search_result["search_time"]/60],
                index=['Parameters grid', 'Best parameters', 'Best scores', 'Search time(min)'
            ])
            f.write(f'\n\n### {grid_search_result["name"]}\n')
            f.write(grid_search_result['key_results'].to_markdown())
            f.write('\n------------------------------------------------------------------------------------------------------')
    print(f'--- data is saved to {file_path} ---')


def concatenate_estimators_scores(grid_search_results, score_key=KEY_BEST_ESTIMATOR_SCORES):
    """
    Concatenate the scores DataFrames from multiple grid search results into a single DataFrame.

    Args:
        grid_search_results (list[dict]): List of grid search result dictionaries, each containing a DataFrame of scores.
        score_key (str): The key in each result dict that contains the DataFrame to concatenate. Default is KEY_BEST_ESTIMATOR_SCORES.

    Returns:
        pd.DataFrame: Concatenated DataFrame with an added 'Model name' column indicating the source model.
    """
    dfs = []
    for grid_search_result in grid_search_results:
        df = grid_search_result[score_key].copy()
        df['Model name'] = grid_search_result['name']
        dfs.append(df)
    return pd.concat(dfs)


def create_tables_of_scores_by_param(grid_search_results, par_names, key, score='roc_auc'):
    """
    Used to create a table of scores by parameters' values for each grid search result.
    """
    def define_param_name(grid_search_result, par_name):
        if par_name in flatten_list_of_dicts(grid_search_result['grid_search'].param_grid):
            return par_name
        else:
            return f'{grid_search_result["name"]}__{par_name}'
        
    def get_best_params_value(grid_search_result, param_name):
        best_params_ = grid_search_result['grid_search'].best_params_
        if param_name not in best_params_:
            return "-"
        sub_params = {name_.split('__')[-1]: value for name_, value in best_params_.items() if f'{param_name}__' in name_}
        if not sub_params:
            res_str =  f"{best_params_[param_name]}"
        else:
            res_str =  f"{best_params_[param_name]} ({sub_params})"
        return res_str

    best_params = {}
    for grid_search_result in grid_search_results:
        model_name = grid_search_result['name']
        if isinstance(par_names, str):
            param_name = define_param_name(grid_search_result, par_names)
            grid_search_result[key] = cv_scores(grid_search_result['grid_search'], score=score, par_names=param_name)
            best_params[model_name] = get_best_params_value(grid_search_result, param_name)
        else:
            param_names = [define_param_name(grid_search_result, par_name) for par_name in par_names]
            grid_search_result[key] = cv_scores_per_params(grid_search_result['grid_search'], score=score, par_names=param_names)
            best_params[model_name] = {par_name: get_best_params_value(grid_search_result, par_name) for par_name in param_names}

    
    res_df = concatenate_estimators_scores(grid_search_results, score_key=key)
    
    return res_df, best_params


def print_scores_by_param(res_df, best_params, title, score='roc_auc', param_values_prune=None, model_names_prune=None ):
    """
    Print a formatted table of splitwise mean scores for each parameter value and the best value for other parameters.

    Args:
        res_df (pd.DataFrame): DataFrame containing the scores to be printed.
        best_params (dict): Dictionary mapping model names to their best parameter values.
        title (str): Title describing the parameter(s) being analyzed.
        score (str, optional): The score metric to display. Defaults to 'roc_auc'.
        param_values_prune (int, optional): Number of characters to display for parameter values. If None, no pruning.
        model_names_prune (int, optional): Number of characters to display for model names. If None, no pruning.

    Returns:
        None
    """
    print(f'****Splitwise mean of {paint(score, format)} scores for each {title} and the best value for the other parametrs****\n')
    for model_name, best_param in best_params.items():
        print(f"Best parameters: {paint(model_name, format)}: {best_param}")
    print('\n========================================================================================================')

    to_print_df = res_df.pivot(columns='Model name').swaplevel(axis='columns').sort_index(axis='columns', level=0, sort_remaining=False)
    to_print_df = to_print_df.rename(columns=lambda x: x[:model_names_prune], level='Model name')
    to_print_df = to_print_df.rename(index=lambda x: x[:param_values_prune] if isinstance(x, str) else x)
    print(to_print_df)

    
def plot_validation_by(df_to_plot, by, score_to_plot='roc_auc', hue='Model name', figsize=(11, 4), rotation_ticks=False, by_axis='x', **kwargs):
    value_vars=['train', 'test']
    id_vars=[c for c in df_to_plot.columns if c not in value_vars]
    df_to_plot = df_to_plot.melt(id_vars=id_vars, value_vars=value_vars, var_name='set', value_name=score_to_plot)
    if by_axis == 'x':
        x_axis, y_axis = by, score_to_plot
    else:
        x_axis, y_axis = score_to_plot, by
        if 'orient' not in kwargs:
            kwargs['orient'] = 'y'
    snsplot = lineplot(df_to_plot, x=x_axis,  y=y_axis, style='set', hue=hue, title=f'{score_to_plot} by {by}s', figsize=figsize, rotation_ticks=rotation_ticks, **kwargs) 
    snsplot.figure.tight_layout()
    return snsplot


def create_train_test_comparation_tables(grid_search_results, params_names):
    comparation_tables = {}
    best_params = {}
    for param_name in params_names:
        param_comparation, best_param = create_tables_of_scores_by_param(grid_search_results, par_names=param_name, key=f'rocauc_by_{param_name}')
        param_comparation_accuracy, _ = create_tables_of_scores_by_param(grid_search_results, par_names=param_name, score='accuracy', key=f'accuracy_by_{param_name}')
        param_comparation = pd.concat([param_comparation, param_comparation_accuracy], axis=0, keys=['roc_auc', 'accuracy']).reset_index(level=0, names='score') 
        comparation_tables[param_name] = param_comparation
        best_params[param_name] = best_param
    return comparation_tables, best_params