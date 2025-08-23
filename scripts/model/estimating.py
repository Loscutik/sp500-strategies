
class WrapModelTrainSizeParam:
    """
    WrapModelTrainSizeParam is a wrapper class for a machine learning model that allows specifying a training size parameter.
    Attributes:
        train_length (int): The length of the training data.
        model (class): The machine learning model class to be wrapped.
        kwargs (dict): Additional keyword arguments to be passed to the model.
    Methods:
        get_params(deep=True):
            Get parameters for this estimator.
            Args:
                deep (bool): If True, will return the parameters for this estimator and contained subobjects that are estimators.
            Returns:
                dict: Parameter names mapped to their values.
        set_params(**params):
            Set the parameters of this estimator.
            Args:
                **params: The parameters to set in the estimator.
            Returns:
                self: The estimator instance.
        fit(X, y):
            Fit the model according to the given training data.
            Args:
                X (array-like): Training data.
                y (array-like): Target values.
            Returns:
                self: The fitted estimator.
        predict(X):
            Perform classification on samples in X.
            Args:
                X (array-like): Input data.
            Returns:
                array: Predicted class labels for samples in X.
        predict_proba(X):
            Return probability estimates for the test data X.
            Args:
                X (array-like): Input data.
            Returns:
                array: Probability estimates for each class.
        score(X, y):
            Return the mean accuracy on the given test data and labels.
            Args:
                X (array-like): Test data.
                y (array-like): True labels for X.
            Returns:
                float: Mean accuracy of self.predict(X) with respect to y.
    """
    def __init__(self, model=None, train_length=None, **kwargs):  
        self.train_length = train_length  
        self.model = model  
        self.kwargs = kwargs  
        if model is not None:  
            self.model_instance = model(**kwargs)  
            self._set_methods()
        else:  
            self.model_instance = None  
        
    def _set_methods(self):
        if hasattr(self.model_instance, 'predict_proba'):
            self.predict_proba = self.model_instance.predict_proba
        if hasattr(self.model_instance, 'predict_log_proba'):
            self.predict_log_proba = self.model_instance.predict_log_proba
        if hasattr(self.model_instance, 'decision_function'):
            self.decision_function = self.model_instance.decision_function
        if hasattr(self.model_instance, 'feature_importances_'):
            self.feature_importances_ = self.model_instance.feature_importances_
  
    def get_params(self, deep=True):  
        if self.model_instance != None:  
            params = self.model_instance.get_params(deep=deep)  
        else:  
            params = self.kwargs  
        params["train_length"] = self.train_length  
        params["model"] = self.model  
        return params  
  
    def set_params(self, **params):  
        self.train_length = params.pop("train_length",self.train_length)  
        if self.model is None:  
            self.model = params.pop("model")  
            self.model_instance = self.model() 
            self._set_methods() 
        self.model_instance.set_params(**params)  
        return self  
  
    def fit(self, X, y):  
        first_idx = max(0, len(X) - self.train_length)  
        X_used = X[first_idx:]  
        y_used = y[first_idx:]  
        self.model_instance.fit(X_used, y_used) 
        self.classes_ = self.model_instance.classes_ 
        return self  
      
    def predict(self, X):
        return self.model_instance.predict(X)  
    
    # def predict_proba(self, X):
    #     if hasattr(self.model_instance, 'predict_proba'):
    #         return self.model_instance.predict_proba(X)
    #     else:
    #         raise AttributeError("predict_proba not available")
    
    # def decision_function(self, X):
    #     if hasattr(self.model_instance, 'decision_function'):
    #         return self.model_instance.decision_function(X)
    #     else:
    #         raise AttributeError("decision_function not available")
    
    # def predict_log_proba(self, X):
    #     if hasattr(self.model_instance, 'predict_log_proba'):
    #         return self.model_instance.predict_log_proba(X)
    #     else:
    #         raise AttributeError("predict_log_proba not available")
      
    def score(self, X, y):  
        return self.model_instance.score(X, y)  


def run_classifier_grid_search(estimator, Xtrain, ytrain, Xtest=None, ytest=None, scoring='roc_auc',cv=5, refit='roc_auc', return_train_score=True, **kwargs):
    import time
    from sklearn.model_selection import GridSearchCV  
    from sklearn.metrics import accuracy_score, average_precision_score, roc_auc_score, f1_score, recall_score, log_loss, confusion_matrix 

    #print(f'Grid search for {color}{estimator["model"]}{del_format}')
    #print(f'Parameters: {estimator["params"]}')
    #print(f'{scoring=}')
    #print('=========================')
    grid_search = GridSearchCV(
        estimator=estimator['model'],
        param_grid=estimator['params'],
        cv=cv, 
        scoring=scoring, 
        refit=refit,
        n_jobs=-1,
        return_train_score=return_train_score, #set it to False reduces fitting time, but we lose the train scores in cv_results_ 
        verbose=1,
        **kwargs
    )

    start_time = time.perf_counter()
    grid_search.fit(Xtrain, ytrain)

    end_time = time.perf_counter()

    res={
        'search_time': end_time - start_time,   
        'grid_search': grid_search,
    }
 
    if Xtest is not None and ytest is not None:
        res['predict'] = grid_search.predict(Xtest),
        res['predict_prob'] = grid_search.predict_proba(Xtest),
        res['accuracy'] = accuracy_score(ytest,res['predict'])
        res['average_precision'] = average_precision_score(ytest,res['predict_prob'])
        res['f1'] = f1_score(ytest,res['predict'], average='binary')
        res['recall'] = recall_score(ytest,res['predict'], average='binary')
        res['roc_auc'] = roc_auc_score(ytest,res['predict_prob'])
        res['log_loss'] = log_loss(ytest,res['predict_prob'])
        res['confusion_matrix'] = confusion_matrix(ytest,res['predict'])
    
    return res

