from sklearn.model_selection import TimeSeriesSplit

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
