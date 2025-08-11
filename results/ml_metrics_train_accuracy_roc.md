## Select transformer and dimention reducer

### logisticregression
|    | split   | set   | solver   |   C | reduce_dim   | n_components   | transformer                       |   accuracy |    roc_auc |
|---:|:--------|:------|:---------|----:|:-------------|:---------------|:----------------------------------|-----------:|-----------:|
|  0 | split2  | test  | saga     | 1   | FastICA()    | 5              | ordinal_quantile_power            |   0.629    | nan        |
|  1 | split2  | test  | saga     | 1.5 | FastICA()    | 5              | ordinal_quantile_power            |   0.628    | nan        |
|  2 | split5  | test  | saga     | 1   | passthrough  | -              | target_std_quantile_power_kbins_q |   0.568    | nan        |
|  3 | split5  | test  | saga     | 1   | passthrough  | -              | target_quantile_power_kbins_q     |   0.564    | nan        |
|  4 | split6  | test  | saga     | 1   | FastICA()    | 2              | ordinal_max_abs_not_indicators    |   0.546    | nan        |
|  5 | split6  | test  | saga     | 1   | FastICA()    | 2              | ordinal_quantile_power            |   0.546    | nan        |
|  6 | split5  | test  | saga     | 1.5 | FastICA()    | None           | target_quantile_power             | nan        |   0.576605 |
|  7 | split5  | test  | saga     | 1   | FastICA()    | None           | target_quantile_power             | nan        |   0.575773 |
|  8 | split1  | test  | saga     | 1.5 | FastICA()    | None           | drop_quantile_power_kbins_q       | nan        |   0.56497  |
|  9 | split8  | test  | saga     | 1.5 | FastICA()    | 5              | target_max_abs_not_indicators     | nan        |   0.555059 |
| 10 | split8  | test  | saga     | 1   | FastICA()    | 5              | target_max_abs_not_indicators     | nan        |   0.555051 |
| 11 | split7  | test  | saga     | 1   | FastICA()    | 5              | drop_no_transform_digit_cols      | nan        |   0.525987 |
| 12 | split7  | test  | saga     | 1   | FastICA()    | 5              | ordinal_no_transform_digit_cols   | nan        |   0.525987 |
| 13 | split7  | test  | saga     | 1   | passthrough  | -              | drop_quantile_power               |   0.518    | nan        |
| 14 | split7  | test  | saga     | 1.5 | passthrough  | -              | drop_quantile_power               |   0.517    | nan        |
| 15 | split7  | train | saga     | 1   | FastICA()    | None           | target_quantile_power_kbins_q     |   0.532022 | nan        |
| 16 | split7  | train | saga     | 1.5 | FastICA()    | None           | target_quantile_power_kbins_q     |   0.532096 |   0.539721 |
| 17 | split7  | train | saga     | 1.5 | passthrough  | -              | target_quantile_power_kbins_q     | nan        |   0.539275 |
| 18 | split9  | test  | saga     | 1   | FastICA()    | 2              | drop_no_transform_digit_cols      | nan        |   0.530101 |
| 19 | split9  | test  | saga     | 1   | FastICA()    | 8              | ordinal_no_transform_digit_cols   |   0.543    | nan        |
| 20 | split9  | test  | saga     | 1   | FastICA()    | 8              | target_no_transform_digit_cols    |   0.543    | nan        |
| 21 | split9  | test  | saga     | 1.5 | FastICA()    | 2              | target_no_transform_digit_cols    | nan        |   0.530101 |
| 22 | split9  | train | saga     | 1   | FastICA()    | None           | target_std_quantile_power_kbins_q |   0.532721 |   0.538721 |
| 23 | split9  | train | saga     | 1.5 | FastICA()    | None           | target_quantile_power_kbins_q     |   0.532426 |   0.538531 |

### gaussiannb
|    | split   | set   |   var_smoothing | transformer                       | reduce_dim   | n_components   |   accuracy |    roc_auc |
|---:|:--------|:------|----------------:|:----------------------------------|:-------------|:---------------|-----------:|-----------:|
|  0 | split2  | test  |           1e-06 | drop_robust_not_indicators        | FastICA()    | 2              |   0.627    | nan        |
|  1 | split2  | test  |           1e-11 | ordinal_quantile_power            | FastICA()    | 2              |   0.626    | nan        |
|  2 | split1  | test  |           1e-06 | ordinal_standard_robust           | FastICA()    | 8              |   0.561    | nan        |
|  3 | split6  | test  |           1e-11 | ordinal_no_transform_digit_cols   | FastICA()    | 2              |   0.561    | nan        |
|  4 | split6  | test  |           1e-11 | target_no_transform_digit_cols    | FastICA()    | 2              |   0.561    | nan        |
|  5 | split5  | test  |           1e-09 | target_standard_not_indicators    | FastICA()    | None           | nan        |   0.566628 |
|  6 | split1  | test  |           1e-09 | ordinal_quantile_power_kbins_u    | FastICA()    | 8              | nan        |   0.566202 |
|  7 | split5  | test  |           1e-11 | target_quantile_power_kbins_q     | FastICA()    | None           | nan        |   0.565913 |
|  8 | split1  | test  |           1e-06 | ordinal_standard_not_indicators   | FastICA()    | 8              | nan        |   0.56557  |
|  9 | split6  | test  |           1e-06 | ordinal_max_abs_not_indicators    | FastICA()    | 2              | nan        |   0.561573 |
| 10 | split7  | test  |           1e-06 | drop_no_transform_digit_cols      | FastICA()    | 2              | nan        |   0.528819 |
| 11 | split7  | test  |           1e-09 | ordinal_no_transform_digit_cols   | FastICA()    | 2              | nan        |   0.528827 |
| 12 | split7  | test  |           1e-11 | ordinal_no_transform_digit_cols   | FastICA()    | 2              |   0.527    | nan        |
| 13 | split7  | test  |           1e-11 | target_no_transform_digit_cols    | FastICA()    | 2              |   0.527    | nan        |
| 14 | split7  | train |           1e-06 | target_std_quantile_power_kbins_q | FastICA()    | None           |   0.525882 |   0.533019 |
| 15 | split7  | train |           1e-09 | target_quantile_power_kbins_q     | FastICA()    | None           | nan        |   0.531478 |
| 16 | split7  | train |           1e-11 | target_quantile_power_kbins_q     | FastICA()    | None           |   0.526838 | nan        |
| 17 | split9  | test  |           1e-06 | target_standard                   | FastICA()    | 8              | nan        |   0.528976 |
| 18 | split9  | test  |           1e-11 | drop_quantile_power_kbins_u       | FastICA()    | 8              | nan        |   0.5271   |
| 19 | split9  | test  |           1e-11 | ordinal_standard_not_indicators   | FastICA()    | 8              |   0.551    | nan        |
| 20 | split9  | test  |           1e-11 | target_standard                   | FastICA()    | 8              |   0.55     | nan        |
| 21 | split9  | train |           1e-06 | target_quantile_power_kbins_q     | FastICA()    | None           |   0.527647 | nan        |
| 22 | split9  | train |           1e-06 | target_std_quantile_power_kbins_q | FastICA()    | None           | nan        |   0.531606 |
| 23 | split9  | train |           1e-09 | target_std_quantile_power_kbins_q | FastICA()    | None           |   0.527684 | nan        |
| 24 | split9  | train |           1e-11 | target_std_quantile_power_kbins_q | FastICA()    | None           | nan        |   0.531228 |

### randomforestclassifier
|    | split   | set   | transformer                        | max_depth   | reduce_dim   | n_components   |   accuracy |    roc_auc |
|---:|:--------|:------|:-----------------------------------|:------------|:-------------|:---------------|-----------:|-----------:|
|  0 | split2  | test  | ordinal_max_abs_not_indicators     | 2           | FastICA()    | 5              |      0.635 | nan        |
|  1 | split2  | test  | target_standard                    | 2           | FastICA()    | 5              |      0.635 | nan        |
|  2 | split6  | test  | target_no_transform_digit_cols     | 2           | FastICA()    | 2              |      0.563 | nan        |
|  3 | split6  | test  | ordinal_no_transform_digit_cols    | 2           | FastICA()    | 2              |      0.562 | nan        |
|  4 | split5  | test  | drop_quantile_power                | None        | FastICA()    | None           |      0.56  | nan        |
|  5 | split5  | test  | target_standard_robust             | 2           | FastICA()    | None           |    nan     |   0.584012 |
|  6 | split5  | test  | ordinal_standard_robust            | 2           | passthrough  | -              |    nan     |   0.576981 |
|  7 | split1  | test  | drop_standard_not_indicators       | 2           | FastICA()    | 8              |    nan     |   0.568687 |
|  8 | split1  | test  | drop_standard_not_indicators       | 2           | FastICA()    | 5              |    nan     |   0.564901 |
|  9 | split8  | test  | drop_standard_not_indicators       | 2           | FastICA()    | 2              |    nan     |   0.564803 |
| 10 | split7  | test  | drop_std_quantile_power_kbins_q    | None        | FastICA()    | 2              |      0.529 | nan        |
| 11 | split7  | test  | ordinal_std_quantile_power_kbins_q | None        | FastICA()    | None           |      0.528 | nan        |
| 12 | split7  | test  | target_no_transform_digit_cols     | 2           | FastICA()    | 2              |    nan     |   0.538713 |
| 13 | split7  | test  | target_no_transform_digit_cols     | None        | FastICA()    | 5              |    nan     |   0.534069 |
| 14 | split7  | train | ordinal_quantile_power_kbins_u     | None        | FastICA()    | 2              |      1     |   1        |
| 15 | split7  | train | ordinal_std_quantile_power_kbins_u | None        | FastICA()    | 2              |      1     |   1        |
| 16 | split9  | test  | drop_quantile_power_kbins_u        | 2           | FastICA()    | 5              |      0.55  | nan        |
| 17 | split9  | test  | drop_quantile_power_kbins_u        | None        | FastICA()    | None           |    nan     |   0.564145 |
| 18 | split9  | test  | ordinal_no_transform_digit_cols    | None        | FastICA()    | 5              |      0.548 |   0.547615 |
| 19 | split9  | train | ordinal_no_transform_digit_cols    | None        | FastICA()    | 2              |      1     | nan        |
| 20 | split9  | train | ordinal_quantile_power_kbins_q     | None        | FastICA()    | 2              |    nan     |   1        |
| 21 | split9  | train | ordinal_std_quantile_power_kbins_u | None        | FastICA()    | 2              |      1     |   1        |

### histgradientboostingclassifier
|    | split   | set   | transformer                        | reduce_dim   | max_depth   | n_components   |   accuracy |    roc_auc |
|---:|:--------|:------|:-----------------------------------|:-------------|:------------|:---------------|-----------:|-----------:|
|  0 | split2  | test  | ordinal_quantile_power             | FastICA()    | 5           | 5              |   0.625    | nan        |
|  1 | split2  | test  | target_max_abs_not_indicators      | FastICA()    | 5           | 8              |   0.623    | nan        |
|  2 | split5  | test  | target_robust_not_indicators       | FastICA()    | 5           | None           |   0.561    | nan        |
|  3 | split6  | test  | drop_quantile_power_kbins_u        | FastICA()    | None        | 8              |   0.561    | nan        |
|  4 | split5  | test  | target_standard_robust             | FastICA()    | 5           | None           |   0.56     | nan        |
|  5 | split2  | test  | target_quantile_power_kbins_q      | FastICA()    | None        | 5              | nan        |   0.571879 |
|  6 | split5  | test  | ordinal_no_transform_digit_cols    | FastICA()    | 5           | 5              | nan        |   0.569402 |
|  7 | split10 | test  | drop_std_quantile_power_kbins_u    | FastICA()    | 5           | 8              | nan        |   0.568561 |
|  8 | split5  | test  | ordinal_quantile_power             | FastICA()    | 5           | None           | nan        |   0.566482 |
|  9 | split1  | test  | target_quantile_power              | FastICA()    | None        | 8              | nan        |   0.562149 |
| 10 | split7  | test  | drop_no_transform_digit_cols       | FastICA()    | 5           | 2              | nan        |   0.537153 |
| 11 | split7  | test  | drop_no_transform_digit_cols       | FastICA()    | None        | None           |   0.532    |   0.539103 |
| 12 | split7  | test  | drop_quantile_power_kbins_u        | FastICA()    | None        | None           |   0.531    | nan        |
| 13 | split7  | train | drop_standard                      | FastICA()    | None        | None           |   0.645331 |   0.732648 |
| 14 | split7  | train | target_quantile_power              | passthrough  | None        | -              |   0.653051 |   0.732806 |
| 15 | split9  | test  | drop_robust_not_indicators         | FastICA()    | 5           | 5              |   0.556    | nan        |
| 16 | split9  | test  | drop_robust_not_indicators         | FastICA()    | 5           | None           |   0.554    | nan        |
| 17 | split9  | test  | drop_standard_robust               | FastICA()    | None        | None           | nan        |   0.557055 |
| 18 | split9  | test  | ordinal_std_quantile_power_kbins_q | FastICA()    | None        | 8              | nan        |   0.544303 |
| 19 | split9  | train | drop_max_abs_not_indicators        | passthrough  | None        | -              |   0.640221 | nan        |
| 20 | split9  | train | drop_robust_not_indicators         | FastICA()    | None        | None           | nan        |   0.721812 |
| 21 | split9  | train | ordinal_std_quantile_power_kbins_q | FastICA()    | None        | None           |   0.652684 |   0.728109 |
## CV 25 folds, 11 days validation

### logisticregression
|    | split   | set   | solver   |   C | reduce_dim   |   n_components |   train_length | transformer                              |   accuracy |    roc_auc |
|---:|:--------|:------|:---------|----:|:-------------|---------------:|---------------:|:-----------------------------------------|-----------:|-----------:|
|  0 | split11 | test  | saga     | 1.5 | FastICA()    |              2 |          27200 | ordinal_std_quantile_power_kbins_u       |   0.643182 | nan        |
|  1 | split11 | test  | saga     | 1.5 | FastICA()    |              2 |          27200 | ordinal_std_quantile_power_kbins_u20     |   0.643182 | nan        |
|  2 | split5  | test  | saga     | 1.5 | FastICA()    |              2 |          23680 | ordinal_quantile_power_kbins_u           |   0.638636 | nan        |
|  3 | split5  | test  | saga     | 1.5 | FastICA()    |              2 |          23680 | ordinal_std_quantile_power_kbins_u       |   0.636364 | nan        |
|  4 | split13 | test  | saga     | 1.5 | FastICA()    |              2 |          23680 | ordinal_std_quantile_power_kbins_u       |   0.611364 | nan        |
|  5 | split13 | test  | saga     | 1.5 | FastICA()    |              2 |          23680 | ordinal_std_quantile_power_kbins_u20     |   0.611364 | nan        |
|  6 | split9  | test  | saga     | 1.5 | FastICA()    |              2 |          20160 | ordinal_quantile_power_kbins_u_scl       | nan        |   0.56453  |
|  7 | split9  | test  | saga     | 1.5 | FastICA()    |              2 |          20160 | ordinal_quantile_power_kbins_u20         | nan        |   0.564117 |
|  8 | split13 | test  | saga     | 1.5 | FastICA()    |              2 |          27200 | ordinal_std_quantile_power_kbins_u20     | nan        |   0.56373  |
|  9 | split13 | test  | saga     | 1.5 | FastICA()    |              2 |          27200 | ordinal_quantile_power_kbins_u20_scl     | nan        |   0.563512 |
| 10 | split2  | test  | saga     | 1.5 | FastICA()    |              2 |          20160 | ordinal_quantile_power_kbins_u20         | nan        |   0.556128 |
| 11 | split7  | test  | saga     | 1.5 | FastICA()    |              2 |          20160 | ordinal_quantile_power_kbins_u           |   0.520455 | nan        |
| 12 | split7  | test  | saga     | 1.5 | FastICA()    |              2 |          20160 | ordinal_quantile_power_kbins_u_scl       |   0.520455 | nan        |
| 13 | split7  | test  | saga     | 1.5 | FastICA()    |              2 |          23680 | ordinal_std_quantile_power_kbins_u20     | nan        |   0.527881 |
| 14 | split7  | test  | saga     | 1.5 | FastICA()    |              2 |          23680 | ordinal_std_quantile_power_kbins_u20_scl | nan        |   0.527633 |
| 15 | split7  | train | saga     | 1.5 | FastICA()    |              2 |          20160 | ordinal_quantile_power_kbins_u20_scl     | nan        |   0.510264 |
| 16 | split7  | train | saga     | 1.5 | FastICA()    |              2 |          20160 | ordinal_std_quantile_power_kbins_u20_scl |   0.520662 | nan        |
| 17 | split7  | train | saga     | 1.5 | FastICA()    |              2 |          27200 | ordinal_quantile_power_kbins_u20         | nan        |   0.510318 |
| 18 | split7  | train | saga     | 1.5 | FastICA()    |              2 |          27200 | ordinal_std_quantile_power_kbins_u       |   0.520662 | nan        |
| 19 | split9  | test  | saga     | 1.5 | FastICA()    |              2 |          20160 | ordinal_quantile_power_kbins_u20         | nan        |   0.564117 |
| 20 | split9  | test  | saga     | 1.5 | FastICA()    |              2 |          20160 | ordinal_quantile_power_kbins_u_scl       | nan        |   0.56453  |
| 21 | split9  | test  | saga     | 1.5 | FastICA()    |              2 |          23680 | ordinal_quantile_power_kbins_u           |   0.495455 | nan        |
| 22 | split9  | test  | saga     | 1.5 | FastICA()    |              2 |          23680 | ordinal_std_quantile_power_kbins_u       |   0.495455 | nan        |
| 23 | split9  | train | saga     | 1.5 | FastICA()    |              2 |          27200 | ordinal_quantile_power_kbins_u           | nan        |   0.510783 |
| 24 | split9  | train | saga     | 1.5 | FastICA()    |              2 |          27200 | ordinal_quantile_power_kbins_u20         |   0.520257 | nan        |
| 25 | split9  | train | saga     | 1.5 | FastICA()    |              2 |          27200 | ordinal_quantile_power_kbins_u20_scl     |   0.520221 |   0.510778 |

### gaussiannb
|    | split   | set   |   var_smoothing | reduce_dim   |   train_length |   n_components | transformer     |   accuracy |    roc_auc |
|---:|:--------|:------|----------------:|:-------------|---------------:|---------------:|:----------------|-----------:|-----------:|
|  0 | split11 | test  |           1e-06 | FastICA()    |          20160 |              2 | target_standard |   0.606818 | nan        |
|  1 | split11 | test  |           1e-11 | FastICA()    |          20160 |              2 | target_standard |   0.606818 | nan        |
|  2 | split13 | test  |           1e-06 | FastICA()    |          23680 |              2 | target_standard |   0.604545 | nan        |
|  3 | split13 | test  |           1e-11 | FastICA()    |          23680 |              2 | target_standard |   0.602273 | nan        |
|  4 | split21 | test  |           1e-06 | FastICA()    |          27200 |              2 | target_standard |   0.590909 | nan        |
|  5 | split21 | test  |           1e-11 | FastICA()    |          27200 |              2 | target_standard |   0.590909 | nan        |
|  6 | split9  | test  |           1e-11 | FastICA()    |          27200 |              2 | target_standard | nan        |   0.575585 |
|  7 | split9  | test  |           1e-06 | FastICA()    |          27200 |              2 | target_standard | nan        |   0.575502 |
|  8 | split13 | test  |           1e-11 | FastICA()    |          20160 |              2 | target_standard | nan        |   0.562295 |
|  9 | split13 | test  |           1e-06 | FastICA()    |          20160 |              2 | target_standard | nan        |   0.562251 |
| 10 | split8  | test  |           1e-06 | FastICA()    |          20160 |              2 | target_standard | nan        |   0.549685 |
| 11 | split7  | test  |           1e-06 | FastICA()    |          27200 |              2 | target_standard | nan        |   0.512959 |
| 12 | split7  | test  |           1e-11 | FastICA()    |          20160 |              2 | target_standard |   0.515909 | nan        |
| 13 | split7  | test  |           1e-11 | FastICA()    |          23680 |              2 | target_standard |   0.515909 | nan        |
| 14 | split7  | test  |           1e-11 | FastICA()    |          27200 |              2 | target_standard | nan        |   0.512938 |
| 15 | split7  | train |           1e-06 | FastICA()    |          23680 |              2 | target_standard |   0.520882 | nan        |
| 16 | split7  | train |           1e-06 | FastICA()    |          27200 |              2 | target_standard | nan        |   0.508692 |
| 17 | split7  | train |           1e-11 | FastICA()    |          23680 |              2 | target_standard |   0.520846 | nan        |
| 18 | split7  | train |           1e-11 | FastICA()    |          27200 |              2 | target_standard | nan        |   0.508691 |
| 19 | split9  | test  |           1e-06 | FastICA()    |          23680 |              2 | target_standard |   0.531818 | nan        |
| 20 | split9  | test  |           1e-06 | FastICA()    |          27200 |              2 | target_standard | nan        |   0.575502 |
| 21 | split9  | test  |           1e-11 | FastICA()    |          23680 |              2 | target_standard |   0.531818 | nan        |
| 22 | split9  | test  |           1e-11 | FastICA()    |          27200 |              2 | target_standard | nan        |   0.575585 |
| 23 | split9  | train |           1e-06 | FastICA()    |          23680 |              2 | target_standard |   0.520368 | nan        |
| 24 | split9  | train |           1e-06 | FastICA()    |          27200 |              2 | target_standard | nan        |   0.509815 |
| 25 | split9  | train |           1e-11 | FastICA()    |          23680 |              2 | target_standard |   0.520368 | nan        |
| 26 | split9  | train |           1e-11 | FastICA()    |          27200 |              2 | target_standard | nan        |   0.509818 |

### randomforestclassifier
|    | split   | set   | reduce_dim   |   n_estimators |   n_components |   max_depth |   train_length | transformer                              |   accuracy |    roc_auc |
|---:|:--------|:------|:-------------|---------------:|---------------:|------------:|---------------:|:-----------------------------------------|-----------:|-----------:|
|  0 | split5  | test  | FastICA()    |            100 |              2 |           2 |          20160 | ordinal_std_quantile_power_kbins_q_scl   |   0.659091 | nan        |
|  1 | split5  | test  | FastICA()    |            100 |              2 |           2 |          20160 | ordinal_std_quantile_power_kbins_q20     |   0.656818 | nan        |
|  2 | split11 | test  | FastICA()    |            100 |              2 |           2 |          27200 | ordinal_std_quantile_power_kbins_q_scl   |   0.65     | nan        |
|  3 | split11 | test  | FastICA()    |             50 |              2 |           2 |          20160 | ordinal_std_quantile_power_kbins_q_scl   |   0.65     | nan        |
|  4 | split13 | test  | FastICA()    |            100 |              2 |           2 |          20160 | ordinal_std_quantile_power_kbins_q       |   0.618182 | nan        |
|  5 | split13 | test  | FastICA()    |             50 |              2 |           2 |          20160 | ordinal_quantile_power_kbins_q_scl       | nan        |   0.573273 |
|  6 | split4  | test  | FastICA()    |            100 |              2 |           2 |          27200 | ordinal_std_quantile_power_kbins_q20_scl | nan        |   0.564455 |
|  7 | split13 | test  | FastICA()    |             50 |              2 |           2 |          20160 | ordinal_std_quantile_power_kbins_q_scl   | nan        |   0.564327 |
|  8 | split9  | test  | FastICA()    |            100 |              2 |           2 |          27200 | ordinal_std_quantile_power_kbins_q       | nan        |   0.563693 |
|  9 | split4  | test  | FastICA()    |            100 |              2 |           2 |          27200 | ordinal_quantile_power_kbins_q20         | nan        |   0.562972 |
| 10 | split7  | test  | FastICA()    |            100 |              2 |           2 |          20160 | ordinal_quantile_power_kbins_q20         | nan        |   0.541522 |
| 11 | split7  | test  | FastICA()    |             50 |              2 |           2 |          20160 | ordinal_quantile_power_kbins_q           | nan        |   0.533709 |
| 12 | split7  | test  | FastICA()    |             50 |              2 |           2 |          20160 | ordinal_std_quantile_power_kbins_q20_scl |   0.511364 | nan        |
| 13 | split7  | test  | FastICA()    |             50 |              2 |           2 |          23680 | ordinal_quantile_power_kbins_q20         |   0.513636 | nan        |
| 14 | split7  | train | FastICA()    |            100 |              2 |           2 |          23680 | ordinal_std_quantile_power_kbins_q       | nan        |   0.527296 |
| 15 | split7  | train | FastICA()    |            100 |              2 |           2 |          27200 | ordinal_std_quantile_power_kbins_q_scl   | nan        |   0.527426 |
| 16 | split7  | train | FastICA()    |             50 |              2 |           2 |          20160 | ordinal_quantile_power_kbins_q           |   0.522169 | nan        |
| 17 | split7  | train | FastICA()    |             50 |              2 |           2 |          20160 | ordinal_std_quantile_power_kbins_q_scl   |   0.522316 | nan        |
| 18 | split9  | test  | FastICA()    |            100 |              2 |           2 |          27200 | ordinal_std_quantile_power_kbins_q       | nan        |   0.563693 |
| 19 | split9  | test  | FastICA()    |             50 |              2 |           2 |          20160 | ordinal_quantile_power_kbins_q20         |   0.495455 | nan        |
| 20 | split9  | test  | FastICA()    |             50 |              2 |           2 |          27200 | ordinal_quantile_power_kbins_q20         |   0.497727 | nan        |
| 21 | split9  | test  | FastICA()    |             50 |              2 |           2 |          27200 | ordinal_std_quantile_power_kbins_q20_scl | nan        |   0.560563 |
| 22 | split9  | train | FastICA()    |            100 |              2 |           2 |          20160 | ordinal_std_quantile_power_kbins_q_scl   |   0.522022 | nan        |
| 23 | split9  | train | FastICA()    |            100 |              2 |           2 |          27200 | ordinal_quantile_power_kbins_q20_scl     | nan        |   0.528983 |
| 24 | split9  | train | FastICA()    |            100 |              2 |           2 |          27200 | ordinal_std_quantile_power_kbins_q       | nan        |   0.527667 |
| 25 | split9  | train | FastICA()    |             50 |              2 |           2 |          20160 | ordinal_std_quantile_power_kbins_q       |   0.521801 | nan        |

### histgradientboostingclassifier
|    | split   | set   | reduce_dim   |   train_length | max_depth   |   n_components | transformer                              |   accuracy |    roc_auc |
|---:|:--------|:------|:-------------|---------------:|:------------|---------------:|:-----------------------------------------|-----------:|-----------:|
|  0 | split11 | test  | FastICA()    |          27200 | None        |              2 | ordinal_std_quantile_power_kbins_u20_scl |   0.620455 | nan        |
|  1 | split11 | test  | FastICA()    |          23680 | 10          |              2 | ordinal_std_quantile_power_kbins_u20     |   0.618182 | nan        |
|  2 | split5  | test  | FastICA()    |          20160 | None        |              2 | ordinal_std_quantile_power_kbins_u       |   0.615909 | nan        |
|  3 | split5  | test  | FastICA()    |          20160 | 10          |              2 | ordinal_std_quantile_power_kbins_u20     |   0.611364 | nan        |
|  4 | split13 | test  | FastICA()    |          27200 | None        |              2 | ordinal_std_quantile_power_kbins_u20     |   0.602273 | nan        |
|  5 | split1  | test  | FastICA()    |          27200 | None        |              2 | ordinal_std_quantile_power_kbins_u       | nan        |   0.57456  |
|  6 | split4  | test  | FastICA()    |          23680 | None        |              2 | ordinal_std_quantile_power_kbins_u_scl   | nan        |   0.57127  |
|  7 | split4  | test  | FastICA()    |          20160 | None        |              2 | ordinal_std_quantile_power_kbins_u20     | nan        |   0.571011 |
|  8 | split24 | test  | FastICA()    |          27200 | 10          |              2 | ordinal_std_quantile_power_kbins_u_scl   | nan        |   0.57088  |
|  9 | split9  | test  | FastICA()    |          20160 | None        |              2 | ordinal_std_quantile_power_kbins_u20     | nan        |   0.565615 |
| 10 | split7  | test  | FastICA()    |          23680 | 10          |              2 | ordinal_std_quantile_power_kbins_u_scl   | nan        |   0.540664 |
| 11 | split7  | test  | FastICA()    |          27200 | 10          |              2 | ordinal_std_quantile_power_kbins_u20     |   0.522727 |   0.547671 |
| 12 | split7  | test  | FastICA()    |          27200 | None        |              2 | ordinal_std_quantile_power_kbins_u       |   0.538636 | nan        |
| 13 | split7  | train | FastICA()    |          23680 | None        |              2 | ordinal_std_quantile_power_kbins_u       |   0.559191 |   0.594078 |
| 14 | split7  | train | FastICA()    |          27200 | 10          |              2 | ordinal_std_quantile_power_kbins_u20     |   0.559007 |   0.591868 |
| 15 | split9  | test  | FastICA()    |          20160 | None        |              2 | ordinal_std_quantile_power_kbins_u20     | nan        |   0.565615 |
| 16 | split9  | test  | FastICA()    |          27200 | 10          |              2 | ordinal_std_quantile_power_kbins_u20     |   0.525    | nan        |
| 17 | split9  | test  | FastICA()    |          27200 | None        |              2 | ordinal_std_quantile_power_kbins_u_scl   |   0.520455 |   0.548361 |
| 18 | split9  | train | FastICA()    |          23680 | None        |              2 | ordinal_std_quantile_power_kbins_u20     | nan        |   0.586824 |
| 19 | split9  | train | FastICA()    |          27200 | 10          |              2 | ordinal_std_quantile_power_kbins_u20     |   0.559926 |   0.594503 |
| 20 | split9  | train | FastICA()    |          27200 | None        |              2 | ordinal_std_quantile_power_kbins_u20_scl |   0.556544 | nan        |
## Choose hyperparameters

### logisticregression
|    | split   | set   |   C | solver          |   max_iter |   train_length |   n_components |   accuracy |    roc_auc |
|---:|:--------|:------|----:|:----------------|-----------:|---------------:|---------------:|-----------:|-----------:|
|  0 | split6  | test  | 1.5 | sag             |        100 |         338640 |              2 |   0.552113 | nan        |
|  1 | split6  | test  | 1.5 | newton-cg       |        100 |         338640 |              2 |   0.552032 | nan        |
|  2 | split2  | test  | 1.8 | sag             |        200 |         338640 |              2 |   0.548754 | nan        |
|  3 | split2  | test  | 1   | newton-cholesky |        200 |         338640 |              2 |   0.548673 | nan        |
|  4 | split5  | test  | 1.8 | lbfgs           |        100 |         250994 |              2 |   0.536499 | nan        |
|  5 | split0  | test  | 1.8 | newton-cholesky |        200 |         280210 |              2 | nan        |   0.561555 |
|  6 | split0  | test  | 1.8 | sag             |        200 |         309426 |              2 | nan        |   0.561546 |
|  7 | split5  | test  | 2   | lbfgs           |        100 |         338640 |              2 | nan        |   0.561067 |
|  8 | split5  | test  | 1   | sag             |        200 |         338640 |              2 | nan        |   0.561048 |
|  9 | split8  | test  | 0.5 | newton-cholesky |        100 |         309426 |              2 | nan        |   0.548864 |
| 10 | split7  | test  | 1.5 | sag             |        200 |         250994 |              2 | nan        |   0.488474 |
| 11 | split7  | test  | 1.8 | newton-cg       |        100 |         250994 |              2 |   0.488193 | nan        |
| 12 | split7  | test  | 1.8 | saga            |        100 |         250994 |              2 |   0.488193 | nan        |
| 13 | split7  | test  | 2   | saga            |        200 |         250994 |              2 | nan        |   0.488424 |
| 14 | split7  | train | 0.5 | lbfgs           |        100 |         250994 |              2 |   0.51745  | nan        |
| 15 | split7  | train | 2   | lbfgs           |        100 |         250994 |              2 |   0.517495 | nan        |
| 16 | split7  | train | 2   | saga            |        100 |         309426 |              2 | nan        |   0.513827 |
| 17 | split7  | train | 2   | saga            |        100 |         338640 |              2 | nan        |   0.513827 |
| 18 | split9  | test  | 0.5 | lbfgs           |        200 |         309426 |              2 | nan        |   0.495892 |
| 19 | split9  | test  | 0.5 | saga            |        200 |         338640 |              2 |   0.515743 | nan        |
| 20 | split9  | test  | 1   | lbfgs           |        200 |         338640 |              2 |   0.515823 | nan        |
| 21 | split9  | test  | 1   | newton-cg       |        200 |         309426 |              2 | nan        |   0.495883 |
| 22 | split9  | train | 0.5 | newton-cg       |        200 |         338640 |              2 | nan        |   0.514138 |
| 23 | split9  | train | 1.5 | newton-cholesky |        100 |         280210 |              2 | nan        |   0.51413  |
| 24 | split9  | train | 1.5 | saga            |        100 |         309426 |              2 |   0.516931 | nan        |
| 25 | split9  | train | 2   | sag             |        200 |         338640 |              2 |   0.51691  | nan        |

### sgdclassifier
|    | split   | set   | loss           | penalty    |   train_length |   n_components |   accuracy |    roc_auc |
|---:|:--------|:------|:---------------|:-----------|---------------:|---------------:|-----------:|-----------:|
|  0 | split2  | test  | hinge          | l2         |         250994 |              2 |   0.612872 | nan        |
|  1 | split2  | test  | hinge          | l2         |         280210 |              2 |   0.612872 | nan        |
|  2 | split1  | test  | perceptron     | l1         |         250994 |              2 |   0.56     | nan        |
|  3 | split1  | test  | perceptron     | l1         |         309426 |              2 |   0.56     | nan        |
|  4 | split6  | test  | log_loss       | elasticnet |         280210 |              2 |   0.5567   | nan        |
|  5 | split0  | test  | hinge          | l1         |         250994 |              2 | nan        |   0.561978 |
|  6 | split0  | test  | squared_error  | elasticnet |         338640 |              2 | nan        |   0.561757 |
|  7 | split5  | test  | log_loss       | l1         |         250994 |              2 | nan        |   0.561588 |
|  8 | split5  | test  | log_loss       | l1         |         338640 |              2 | nan        |   0.561533 |
|  9 | split8  | test  | log_loss       | elasticnet |         250994 |              2 | nan        |   0.548632 |
| 10 | split7  | test  | log_loss       | l1         |         280210 |              2 |   0.51494  | nan        |
| 11 | split7  | test  | modified_huber | l1         |         338640 |              2 |   0.51494  | nan        |
| 12 | split7  | test  | modified_huber | l2         |         309426 |              2 | nan        |   0.514596 |
| 13 | split7  | test  | squared_hinge  | l2         |         338640 |              2 | nan        |   0.514505 |
| 14 | split7  | train | hinge          | elasticnet |         338640 |              2 | nan        |   0.513827 |
| 15 | split7  | train | log_loss       | elasticnet |         309426 |              2 |   0.517353 | nan        |
| 16 | split7  | train | squared_hinge  | elasticnet |         338640 |              2 |   0.517408 | nan        |
| 17 | split7  | train | squared_hinge  | l1         |         338640 |              2 | nan        |   0.513818 |
| 18 | split9  | test  | hinge          | l2         |         250994 |              2 |   0.526747 | nan        |
| 19 | split9  | test  | log_loss       | elasticnet |         309426 |              2 |   0.526827 | nan        |
| 20 | split9  | test  | perceptron     | l2         |         280210 |              2 | nan        |   0.503307 |
| 21 | split9  | test  | squared_hinge  | l2         |         280210 |              2 | nan        |   0.504445 |
| 22 | split9  | train | hinge          | l1         |         309426 |              2 | nan        |   0.514121 |
| 23 | split9  | train | log_loss       | elasticnet |         250994 |              2 |   0.517135 | nan        |
| 24 | split9  | train | modified_huber | l1         |         309426 |              2 |   0.516988 | nan        |
| 25 | split9  | train | squared_hinge  | l1         |         338640 |              2 | nan        |   0.514122 |

### randomforestclassifier
|    | split   | set   |   n_estimators |   min_samples_split |   min_samples_leaf | max_features   |   max_depth |   train_length |   n_components |   accuracy |    roc_auc |
|---:|:--------|:------|---------------:|--------------------:|-------------------:|:---------------|------------:|---------------:|---------------:|-----------:|-----------:|
|  0 | split2  | test  |            100 |                   2 |                  2 | log2           |           2 |         338640 |              2 |   0.608436 | nan        |
|  1 | split2  | test  |            200 |                   4 |                  2 | log2           |           2 |         338640 |              2 |   0.608194 | nan        |
|  2 | split6  | test  |            200 |                   4 |                  3 | None           |           3 |         280210 |              2 |   0.557425 | nan        |
|  3 | split6  | test  |            100 |                   2 |                  2 | sqrt           |           3 |         250994 |              2 |   0.556861 | nan        |
|  4 | split3  | test  |            150 |                   2 |                  3 | None           |           2 |         280210 |              2 |   0.54085  | nan        |
|  5 | split0  | test  |            200 |                   2 |                  1 | None           |           2 |         250994 |              2 | nan        |   0.563224 |
|  6 | split0  | test  |            150 |                   2 |                  1 | None           |           2 |         280210 |              2 | nan        |   0.563055 |
|  7 | split5  | test  |            200 |                   2 |                  3 | None           |           3 |         309426 |              2 | nan        |   0.562657 |
|  8 | split5  | test  |            200 |                   2 |                  2 | None           |           3 |         280210 |              2 | nan        |   0.562632 |
|  9 | split6  | test  |            150 |                   3 |                  3 | None           |           3 |         280210 |              2 | nan        |   0.55034  |
| 10 | split7  | test  |            100 |                   3 |                  2 | None           |           3 |         250994 |              2 | nan        |   0.49338  |
| 11 | split7  | test  |            100 |                   4 |                  2 | None           |           2 |         250994 |              2 | nan        |   0.493152 |
| 12 | split7  | test  |            200 |                   2 |                  1 | None           |           3 |         250994 |              2 |   0.486345 | nan        |
| 13 | split7  | test  |            200 |                   3 |                  1 | None           |           3 |         250994 |              2 |   0.486586 | nan        |
| 14 | split7  | train |            100 |                   3 |                  2 | log2           |           3 |         280210 |              2 | nan        |   0.518483 |
| 15 | split7  | train |            200 |                   2 |                  2 | None           |           3 |         250994 |              2 |   0.517915 | nan        |
| 16 | split7  | train |            200 |                   2 |                  3 | None           |           3 |         250994 |              2 |   0.517936 | nan        |
| 17 | split7  | train |            200 |                   3 |                  2 | log2           |           3 |         250994 |              2 | nan        |   0.518243 |
| 18 | split9  | test  |            100 |                   3 |                  1 | sqrt           |           3 |         280210 |              2 |   0.52755  | nan        |
| 19 | split9  | test  |            150 |                   3 |                  1 | None           |           3 |         280210 |              2 | nan        |   0.50273  |
| 20 | split9  | test  |            150 |                   4 |                  3 | sqrt           |           3 |         280210 |              2 |   0.527711 | nan        |
| 21 | split9  | test  |            200 |                   2 |                  1 | None           |           3 |         280210 |              2 | nan        |   0.502824 |
| 22 | split9  | train |            150 |                   2 |                  1 | None           |           3 |         280210 |              2 | nan        |   0.518965 |
| 23 | split9  | train |            200 |                   2 |                  1 | None           |           3 |         309426 |              2 |   0.518379 | nan        |
| 24 | split9  | train |            200 |                   2 |                  2 | None           |           3 |         280210 |              2 | nan        |   0.518964 |
| 25 | split9  | train |            200 |                   3 |                  1 | None           |           3 |         309426 |              2 |   0.518352 | nan        |
## Choose RandomForestClassifier's hyperparameters 

### randomforestclassifier
|    | split   | set   |   n_estimators |   min_samples_leaf | max_features   |   max_depth |   train_length |   n_components |   accuracy |    roc_auc |
|---:|:--------|:------|---------------:|-------------------:|:---------------|------------:|---------------:|---------------:|-----------:|-----------:|
|  0 | split2  | test  |            250 |                  6 | None           |           3 |         265602 |              2 |   0.564239 | nan        |
|  1 | split2  | test  |            300 |                  3 | None           |           4 |         300462 |              2 |   0.563997 | nan        |
|  2 | split6  | test  |            200 |                  6 | None           |           5 |         280210 |              2 |   0.556781 | nan        |
|  3 | split6  | test  |            200 |                  3 | None           |           3 |         280210 |              2 |   0.556539 |   0.5501   |
|  4 | split3  | test  |            250 |                  5 | None           |           3 |         300462 |              2 |   0.539156 | nan        |
|  5 | split0  | test  |            200 |                  6 | None           |           3 |         300462 |              2 | nan        |   0.562588 |
|  6 | split0  | test  |            300 |                  6 | None           |           3 |         280210 |              2 | nan        |   0.56232  |
|  7 | split5  | test  |            200 |                  3 | None           |           5 |         265602 |              2 | nan        |   0.562054 |
|  8 | split5  | test  |            300 |                  5 | None           |           3 |         280210 |              2 | nan        |   0.561932 |
|  9 | split7  | test  |            200 |                  5 | None           |           4 |         265602 |              2 | nan        |   0.491912 |
| 10 | split7  | test  |            200 |                  5 | None           |           5 |         300462 |              2 |   0.488273 | nan        |
| 11 | split7  | test  |            200 |                  6 | None           |           5 |         265602 |              2 | nan        |   0.492104 |
| 12 | split7  | test  |            300 |                  3 | None           |           5 |         300462 |              2 |   0.488353 | nan        |
| 13 | split7  | train |            250 |                  3 | None           |           5 |         300462 |              2 |   0.521732 | nan        |
| 14 | split7  | train |            250 |                  6 | None           |           5 |         300462 |              2 |   0.521894 | nan        |
| 15 | split7  | train |            300 |                  5 | None           |           5 |         265602 |              2 | nan        |   0.525658 |
| 16 | split7  | train |            300 |                  5 | None           |           5 |         280210 |              2 | nan        |   0.525773 |
| 17 | split9  | test  |            200 |                  3 | None           |           3 |         280210 |              2 |   0.52755  | nan        |
| 18 | split9  | test  |            250 |                  3 | None           |           3 |         300462 |              2 |   0.527711 | nan        |
| 19 | split9  | test  |            250 |                  6 | None           |           4 |         265602 |              2 | nan        |   0.502382 |
| 20 | split9  | test  |            300 |                  5 | None           |           4 |         265602 |              2 | nan        |   0.502736 |
| 21 | split9  | train |            250 |                  3 | None           |           5 |         265602 |              2 |   0.521353 | nan        |
| 22 | split9  | train |            250 |                  3 | None           |           5 |         300462 |              2 | nan        |   0.526903 |
| 23 | split9  | train |            300 |                  3 | None           |           5 |         300462 |              2 | nan        |   0.527056 |
| 24 | split9  | train |            300 |                  5 | None           |           5 |         280210 |              2 |   0.521221 | nan        |
## Choose RandomForestClassifier's hyperparameters  after feature analysis

### randomforestclassifier
|    | split   | set   | reduce_dim   | max_features   |   n_estimators |   n_components |   max_depth |   min_samples_leaf | transformer                   |   accuracy |    roc_auc |
|---:|:--------|:------|:-------------|:---------------|---------------:|---------------:|------------:|-------------------:|:------------------------------|-----------:|-----------:|
|  0 | split2  | test  | FastICA()    | None           |            200 |              4 |           3 |                  3 | target_quantile_power_kbins_u |   0.59     | nan        |
|  1 | split2  | test  | FastICA()    | None           |            200 |              4 |           4 |                  3 | target_quantile_power_kbins_u |   0.581    | nan        |
|  2 | split6  | test  | FastICA()    | None           |            200 |              2 |           3 |                  3 | target_quantile_power_kbins_u |   0.578    | nan        |
|  3 | split6  | test  | PCA()        | None           |            200 |              2 |           3 |                  3 | target_quantile_power_kbins_u |   0.578    | nan        |
|  4 | split3  | test  | PCA()        | None           |            200 |              2 |           3 |                  3 | ordinal_quantile_power        |   0.56     | nan        |
|  5 | split5  | test  | PCA()        | None           |            200 |             20 |           3 |                  3 | target_robust_not_indicators  | nan        |   0.592474 |
|  6 | split5  | test  | PCA()        | None           |            200 |             20 |           5 |                  3 | target_robust_not_indicators  | nan        |   0.590105 |
|  7 | split0  | test  | FastICA()    | None           |            200 |              4 |           3 |                  3 | target_robust_not_indicators  | nan        |   0.572504 |
|  8 | split0  | test  | PCA()        | None           |            200 |             10 |           4 |                  3 | ordinal_quantile_power        | nan        |   0.567341 |
|  9 | split8  | test  | FastICA()    | None           |            200 |              4 |           5 |                  3 | target_robust_not_indicators  | nan        |   0.559772 |
| 10 | split7  | test  | FastICA()    | None           |            200 |             10 |           5 |                  3 | ordinal_quantile_power        |   0.503    | nan        |
| 11 | split7  | test  | FastICA()    | None           |            200 |              2 |           3 |                  3 | ordinal_quantile_power        | nan        |   0.522041 |
| 12 | split7  | test  | FastICA()    | None           |            200 |              2 |           5 |                  3 | ordinal_quantile_power        | nan        |   0.530325 |
| 13 | split7  | test  | FastICA()    | None           |            200 |             20 |           3 |                  3 | target_robust_not_indicators  |   0.501    | nan        |
| 14 | split7  | train | FastICA()    | None           |            200 |             20 |           5 |                  3 | target_quantile_power_kbins_u |   0.589273 |   0.669671 |
| 15 | split7  | train | PCA()        | None           |            200 |             20 |           5 |                  3 | ordinal_quantile_power        |   0.58776  |   0.662294 |
| 16 | split9  | test  | FastICA()    | None           |            200 |             10 |           4 |                  3 | target_quantile_power_kbins_u | nan        |   0.510986 |
| 17 | split9  | test  | FastICA()    | None           |            200 |             20 |           4 |                  3 | target_quantile_power_kbins_u |   0.537    | nan        |
| 18 | split9  | test  | PCA()        | None           |            200 |             20 |           5 |                  3 | target_quantile_power_kbins_u | nan        |   0.518322 |
| 19 | split9  | test  | PCA()        | None           |            200 |              4 |           3 |                  3 | target_quantile_power_kbins_u |   0.542    | nan        |
| 20 | split9  | train | FastICA()    | None           |            200 |             20 |           5 |                  3 | ordinal_quantile_power        |   0.592215 |   0.648939 |
| 21 | split9  | train | FastICA()    | None           |            200 |             20 |           5 |                  3 | target_quantile_power_kbins_u |   0.595415 |   0.662985 |
