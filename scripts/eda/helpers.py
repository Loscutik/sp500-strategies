import pandas as pd

class StockOLHCV(pd.DataFrame): 
    """
    StockOLHCV is a subclass of pandas DataFrame designed to handle stock data with specific methods for accessing date and name information from the index.
    Methods
    -------
    dates():
        Returns the 'date' level values from the index if 'date' is one of the index levels, otherwise returns None.
    names():
        Returns the 'Name' level values from the index if 'Name' is one of the index levels, otherwise returns None.
    """
    
    def dates(self):
        if 'date' in self.index.names:
            return self.index.get_level_values('date')
        else:
            return None
    
    def names(self):
        if 'Name' in self.index.names:
            return self.index.get_level_values('Name')
        else:
            return None
        