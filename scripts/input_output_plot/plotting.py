import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns

from collections.abc import Iterable
from helpers import isnumber
import math
import numpy as np
import pandas as pd

from helpers import is_iterable


def get_fig_and_axes(ncols, n_axes, row_high=4, fig_width=12):
    nrows = math.ceil(n_axes / ncols)
    fig, axs = plt.subplots(nrows, ncols, figsize=(fig_width, nrows * row_high))
    axs = axs.flatten()
    return fig, axs


def plot_small_term_orgs(small_term_orgs, bar_colors, max_term):
    fig, ax = plt.subplots(figsize=[15,5])
    rect_tr = ax.bar(small_term_orgs.index, small_term_orgs['n_days'], width=0.5, color=bar_colors)
    plt.xticks(rotation=45)
    plt.ylim(0, max_term*1.3)
    ax.bar_label(rect_tr, labels=small_term_orgs['start'].dt.strftime('%Y/%m/%d'), padding=2, color='green', rotation=90)
    ax.set_ylabel('Number of days')
    ax.set_title('Companies presented in all_stocks_5yr.csv not for the whole term (less than 5 years)')
    date_legend = [mpatches.Patch(color='green', label='Date of appearance in SP500'),
                mpatches.Patch(color='royalblue',label='Start date later than usual'),
                mpatches.Patch(color='yellow', label='Usual start date')]

    ax.legend(handles=date_legend)
    plt.close(fig)
    return fig


def plot_outliers_OLHC_to_pdf(outliers_z_score_OHLC, data_set, outliers_file_name):
    outliers_z_score_OHLC_orgs = outliers_z_score_OHLC.names().unique()
    outliers_z_score_OHLC_orgs_number = outliers_z_score_OHLC_orgs.size

    with PdfPages(outliers_file_name) as pdf:
        for i in range(outliers_z_score_OHLC_orgs_number):
            fig, ax = plt.subplots(1,2,figsize=(15, 4))
            sns.boxplot(data=data_set[data_set.names()==outliers_z_score_OHLC_orgs[i]][['open', 'high', 'low', 'close']], ax=ax[0])
            data_set[data_set.names()==outliers_z_score_OHLC_orgs[i]][['open', 'high', 'low', 'close']].reset_index(level='Name', drop=True).plot(ax=ax[1])
            ax[1].set_ylabel('Stock Price')
        
            fig.suptitle(outliers_z_score_OHLC_orgs[i])
            pdf.savefig()
        # Closing the figure prevents it from being displayed directly inside the notebook.
            if (outliers_z_score_OHLC_orgs[i] not in []): #['RF','VZ', 'XL']
                plt.close(fig)

   
def scatter_Volume(plot_data_grouped):
    fig, ax = plt.subplots(figsize=(15,5))
    cmap=mpl.colormaps['plasma']
    
    for i,(org, gr) in enumerate(plot_data_grouped):
        ax.scatter(gr.index.get_level_values('date') ,gr['volume'], color=cmap(i), s=1)
    plt.xlabel("Date")
    plt.ylabel("Z-Score")
    plt.title("Z-Score of Volume for train set\n(colored by companies)")
    plt.close(fig)
    return fig


def plot_volume_z_scores(df, companies_to_plot, column_name='volume', title=None, ylabel=None):
    plot_df = df[column_name].reset_index('Name')
    fig, ax = plt.subplots(figsize=(15, 6))
    sns.boxplot(x='Name', y=column_name, data=plot_df[plot_df['Name'].isin(companies_to_plot)], ax=ax)
    plt.xticks(rotation=90)
    if title is None:
        title = f'Boxplot of {column_name.capitalize()}'
    if ylabel is None:
        ylabel = f'{column_name.capitalize()}'
    ax.set_title(title)
    ax.set_xlabel('Company')
    ax.set_ylabel(ylabel)
    plt.close(fig)
    return fig


def plot_outliers_Volume_to_pdf(companies_to_plot, z_scores_set, outliers_file_name, z_score_threshold=4.5, quantile_range=(0.1, 0.9), interval_rate=3.5):
    with PdfPages(outliers_file_name) as pdf:
        for org in companies_to_plot:
            plot_data = z_scores_set[z_scores_set.names()==org]['volume']
            plot_z_score = plot_data[plot_data.abs()>z_score_threshold]
            fig, ax = plt.subplots(figsize=(15, 4))
            x = plot_data.index.get_level_values('date')
            ax.plot(x, plot_data, label='Volume Z-Score')
            ax.scatter(x=plot_z_score.index.get_level_values('date'),y=plot_z_score, c='red', label='Z-Score')
            Q1 = plot_data.quantile(quantile_range[0])
            Q3 = plot_data.quantile(quantile_range[1])
            IQR = interval_rate * (Q3 - Q1)
            ax.plot(x, [Q1 - IQR] * len(x), color='yellow', label=f'Q1-{interval_rate}(Q3-Q1)')
            ax.plot(x, [Q3 + IQR] * len(x), color='green', label=f'Q3+{interval_rate}(Q3-Q1)')
            ax.set_ylabel('Z-Scores unit')
            date_legend = [mpatches.Patch(color='blue',label='Volume'),
                        mpatches.Patch(color='yellow', label=f'Q1-{interval_rate}(Q3-Q1)'),
                        mpatches.Patch(color='green', label=f'Q3+{interval_rate}(Q3-Q1)'),
                        mpatches.Patch(color='red', label=f'z-scores (absolute value>{z_score_threshold})'),
                        ]

            ax.legend(handles=date_legend)
            fig.suptitle(org)
            pdf.savefig()
        # Closing the figure prevents it from being displayed directly inside the notebook.
            if (org not in []): #['HSY','O','PVH']
                plt.close(fig)


def set_indexed_ax(ax, nrows, ncols, idx):
    if nrows == 1 and ncols == 1:
        return ax
    if nrows == 1 or ncols == 1:
        return ax[idx]
    return ax[idx//ncols, idx%ncols]


def plot_features_hist(data, features_to_plot, bins=100, ncols=2, suptitle=None, figsize=(12,10)):
    n_features = len(features_to_plot)
    nrows= math.ceil(n_features/ncols)
    fig, ax = plt.subplots(nrows, ncols, figsize=figsize)
    for i, feature in enumerate(features_to_plot):
        curent_ax = set_indexed_ax(ax, nrows, ncols, i)
        sns.histplot(data[feature], bins=bins, kde=True, ax=curent_ax)
        curent_ax.set(
            title=feature.replace('_', ' ').capitalize(),
            xlabel='value',
            )
        if data[feature].abs().max() >= 1000:
            curent_ax.set_yscale('symlog')

    if suptitle is not None:
        fig.suptitle(suptitle, fontsize=16)  
    plt.tight_layout()
    plt.close(fig)
    return fig

    
def plot_features_count(data, features_to_plot, ncols=2, suptitle=None, figsize=(12,10)):
    n_features = len(features_to_plot)
    nrows= math.ceil(n_features/ncols)
    fig, ax = plt.subplots(nrows, ncols, figsize=figsize)
    for i, feature in enumerate(features_to_plot):
        curent_ax = set_indexed_ax(ax, nrows, ncols, i)
        sns.countplot(data=data, x=feature, ax=curent_ax)
        curent_ax.set(
            title=feature.replace('_', ' ').capitalize(),
            xlabel='value',
            )
        curent_ax.bar_label(curent_ax.containers[0], fmt='%.0f')

    if suptitle is not None:
        fig.suptitle(suptitle, fontsize=16)   
    plt.tight_layout()
    plt.close(fig)
    return fig


def plot_cv(cv, title, X, y=None, scale_x=10, lw=10, figsize=([6.4, 4.8])):
    """
    Plots the cross-validation (CV) splits for a given dataset.
    Parameters:
    cv : cross-validation generator
        The cross-validation splitting strategy.
    title : str
        The title of the plot.
    X : array-like
        The input data to be split.
    y : array-like
        The target variable to be split.
    scale_x : int, optional (default=10)
        The scaling factor for the x-axis. It will plot only each `scale_x`-th index. If x is too large, it let decrease execution time.
    lw : int, optional (default=10)
        The line width for the scatter plot markers.
    Returns:
    ax : matplotlib.axes.Axes
        The axes object with the plot.
    tr : array-like
        The training indices for the last CV split.
    tt : array-like
        The testing indices for the last CV split.
    """
    
    fig, ax = plt.subplots(figsize=figsize)
    # Generate the training/testing visualizations for each CV split
    for ii, (tr, tt) in enumerate(cv.split(X=X, y=y)):
        # Fill in indices with the training/test groups
        xlim = len(X)/scale_x
        indices = np.array([np.nan] * math.ceil(len(X)/scale_x))
        indices[np.array(tt[::scale_x])//scale_x] = 1
        indices[np.array(tr[::scale_x])//scale_x] = 0
        #indices[tt] = 1
        #indices[tr] = 0

        # Visualize the results
        ax.scatter(
            range(len(indices)),
            [ii + 0.5] * len(indices),
            c=indices,
            marker="_",
            lw=lw,
            cmap=plt.cm.coolwarm,
            vmin=-0.2,
            vmax=1.2,
        )
        
        # Formatting
    n_splits = cv.get_n_splits()
    yticklabels = list(range(n_splits))
    xticks = ax.get_xticks()[:-1]
    X_idxs = xticks.astype(int)*scale_x
    xticklabels =X_idxs.astype(str)+'\n'+X.index[X_idxs].astype(str)
    ax.set(
        yticks=np.arange(n_splits) + 0.5,
        yticklabels=yticklabels,
        xticks = xticks,
        xticklabels=xticklabels,
        xlabel="Sample index and date",
        ylabel="CV iteration",
        ylim=[n_splits + 0.2, -0.2],
        xlim=[0, len(indices)-1],
    )
    #plt.xticks(rotation=45)
    cv.get_test_ranges()
    ax.set_title(title, fontsize=15)
    plt.close()
    
    return fig


def lineplot(data, x, y='roc_auc', title=None, style='set', hue='Model name', figsize=(10, 6), rotation_ticks=False, **kwargs):

    plt.figure(figsize=figsize)
    if title is None:
        title = f'{y} by {x}'
    plt.title(title)
    if rotation_ticks:
        plt.xticks(rotation=90)
    snsplot = sns.lineplot(data=data, x=x, y=y, style=style, hue=hue, markers=True, dashes=True, legend='brief', **kwargs)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), title=x)
    plt.close()
    return snsplot


def barplot(data, x, y='roc_auc', title=None, hue='set', figsize=(10, 6), rotation_ticks=False):

    plt.figure(figsize=figsize)
    if title is None:
        title = f'{y} by {x}'
    plt.title(title)
    if rotation_ticks:
        plt.xticks(rotation=90)
    snsplot = sns.barplot(data=data, x=x, y=y, hue=hue, legend='brief')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), title=x)
    
    plt.tight_layout()
    plt.close()
    return snsplot


def plot_corr_heatmap(corr_matrix):
    plt.figure(figsize=(12, 10))
    snsplot = sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
    plt.title('Correlation Heatmap (Combined Data)', fontsize=16)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.close()
    return snsplot


def plot_two_features_vs(data, feature_x, feature_y, ax):
    ax.scatter(data[feature_x], data[feature_y], color='skyblue', alpha=0.5)
    correlation = round(data[[feature_x, feature_y]].corr().iloc[0,1], 2)
    ax.set_title(f'{feature_x} vs {feature_y} (correlation={correlation})', fontsize=14)
    ax.set_xlabel(feature_x, fontsize=12)
    ax.set_ylabel(feature_y, fontsize=12)
    ax.tick_params(axis='both', which='major', labelsize=10)
    ax.grid(True, linestyle='--', alpha=0.7)
    return ax


def plot_vs_features(data, fetures_x, fetures_y, ncols=2, figsize=(12, 6)):
    nrows = math.ceil(len(fetures_x) / ncols)
    fig, axs = plt.subplots(nrows, ncols, figsize=figsize)
    axs = axs.flatten()
    for i, (x, y) in enumerate(zip(fetures_x, fetures_y)):
        plot_two_features_vs(data, x, y, axs[i])
    plt.tight_layout()
    plt.close()
    return fig


def plot_boxplot_before_after_capping_outliers(x_before, x_after, figsize=(15, 7), yscale=None):
    import seaborn as sns
    fig, axs = plt.subplots(1,2,figsize=figsize)
    sns.boxplot(data=x_before, palette="Set2",ax=axs[0])
    axs[0].set_title('Box Plot for Features with outliers', fontsize=16)
    sns.boxplot(data=x_after, palette="Set2", ax=axs[1])
    axs[1].set_title('Box Plot for Features with outliers after capping', fontsize=16)

    for ax in axs:
        ax.set_xlabel('Features')
        ax.set_ylabel('Values')
        ax.set_xticks(ax.get_xticks())
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
        # Set y-axis to logarithmic scale
        if yscale is not None:
            ax.set_yscale(yscale)

    # Improve layout
    plt.tight_layout()
    plt.close()
    return fig


def plot_validation_curves(scores_dfs, best_params_, title, rowsize=(12,4), ncols=4, exclude_params=None):
    
    if not  isinstance(exclude_params, Iterable):
        exclude_params = [exclude_params]
    params_to_plot = [param for param in scores_dfs.keys() if param not in exclude_params]
    
    nrows=math.ceil(len(params_to_plot)/ncols)
    figsize =(rowsize[0], nrows*rowsize[1])
    fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize)
    ax = ax.flatten()
    fig.suptitle(title)
    mins = [df.min().min() for df in scores_dfs.values()]
    maxs = [df.max().max() for df in scores_dfs.values()]
    y_min = min(mins)
    y_max = max(maxs)
    y_min = y_min - 0.1 * (y_max - y_min)
    y_max = y_max + 0.1 * (y_max - y_min)
   
    for i, param in enumerate(params_to_plot):
        df = scores_dfs[param]
        ax[i].set_title(param.split('__')[1])
        
        if isnumber(df.index[0]):
            ax[i].plot(df.index, df['train'], label="training score")
            ax[i].plot(df.index, df['test'], label="cross validation score")
        else:
            ax[i].scatter(df.index, df['train'], label="training score")
            ax[i].scatter(df.index, df['test'], label="cross validation score")

        best_value = best_params_[param]
        if best_value is not None:
            ax[i].scatter(x=[best_value], y=y_min + 0.1 * (y_max - y_min), c='green', marker='*', label='best value')
        else:
            x_min, x_max = ax[i].get_xbound()
            y_min, y_max = ax[i].get_ybound()
            ax[i].text(x_min + 0.1 * (x_max - x_min),
                          y_min + 0.1 * (y_max - y_min),
                          'Best: None', label='best value')
        ax[i].sharey(ax[0])
        if i != 0:
            ax[i].tick_params(left=False, labelleft=False)

        ax[i].tick_params(axis='x', rotation=45)
    for j in range(i+1, len(ax)):
        ax[j].axis('off')
    ax[0].set_ylabel("Score: ROC AUC")
    plt.ylim(y_min, y_max)
    handles, labels = ax[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='center left', bbox_to_anchor=(0.8, 1/(2*nrows)))

    plt.tight_layout()
    plt.close()
    return fig


def plot_learning_curves(X, y, estimators, cv, ncols=3, fig_width=17, rowsize=5):
    from sklearn.model_selection import LearningCurveDisplay
    count_params = {
        "X": X,
        "y": y,
        "train_sizes": np.linspace(0.1, 1.0, 5),  #it is the default value
        "cv": cv,
        "scoring": "roc_auc",
        "n_jobs": -1,
    }
    plot_params = {
        "line_kw": {"marker": "o"},
        #default=”fill_between” -The style used to display the score standard deviation around the mean score. If None, no representation of the standard deviation is displayed.
        "std_display_style": "fill_between",
        # The name of the score used to decorate the y-axis of the plot. It will override the name inferred from the scoring parameter.
        "score_name": "Score: ROC_AUC",
    }

    def plot(estimator, est_name, ax=None):
        # score_type is the type of score to plot. Can be one of "test", "train", or "both".
        LearningCurveDisplay.from_estimator(estimator, **count_params, score_type="both", **plot_params, ax=ax)
        if ax is None:
            plt.title(f'Learning curve of {est_name}')
        else:
            ax.set_title(f'Learning curve of {est_name}')
    
    if len(estimators.keys()) == 1:
        fig, ax = plt.subplots(figsize=(fig_width, rowsize), sharey=True)
        est_name = list(estimators.keys())[0]
        plot(estimators[est_name], est_name, ax=ax)
    else:
        nrows = math.ceil(len(estimators.keys()) / ncols)
        fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=(fig_width, rowsize * nrows), sharey=True)
        axs = axs.flatten()

        for i, (estimator, est_name) in enumerate(estimators.items()):
            plot(estimator, est_name, ax=ax[i])
    plt.tight_layout()
    plt.close()
    return fig

