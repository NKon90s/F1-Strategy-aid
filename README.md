# F1 Strategy Aid 
  
This project aims to serve as an aid for F1 tyre strategy decisions. It helps to determine the initial tyre and pit stop strategy via machine learning tools and race simulation techniques. The base data is fetched from [OpenF1 Api](https://openf1.org/). 


## Table of contents 




## Requirements 

For specific requirements and dependencies, please read the `requirements.txt` file.
Use for example `pip install` method. E.g:  `pip install -r requirements.txt`

But the docker containers handle the dependencies automatically.


## ELT Pipeline

Training data is ingested through an ELT pipeline. Data is extracted from the `OpenF1 API` using Python’s `requests library` and loaded into a `PostgreSQL database`. Data cleaning, basic data engineering, and transformations are performed using `dbt`. The entire workflow is orchestrated with `Apache Airflow` and containerized using `Docker`. 

The schema of the pipeline:

![ELT pipeline](imgs/ETLpipeline.png)

**The following databases have been created via the ELT pipeline:**

The following databases have been used to create the training data. The staging tables are the results of Open F1 endpoint requests. The intermediate and mart tables are the transformed, engineered tables. 

- **staging**:
    - stg_car_data
    - stg_drivers
    - stg_intervals
    - stg_laps
    - stg_meetings
    - stg_pit
    - stg_position
    - stg_race_control
    - stg_sesssions
    - stg_starting_grid
    - stg_stints
    - stg_weather
- **intermediate**:
    - int_lap_enriched
    - int_race_context
    - int_start_strategy
    - int_tyre_degradation
- **marts**: 
    - mart_start_strategy_features
    - mart_strategy_prediction_features
    - mart_tyre_prediction_features


## The prediction models

(At the moment) Two machine learning models form the foundation of the race strategy determination process: a starting compound prediction model and a first-stint prediction model. Both models are based on the `XGBoost framework`, with `XGBClassifier` used to predict the starting tyre compound and `XGBRegressor` employed to estimate the duration of the first stint.

In addition, `Linear Regression` is used during feature engineering to estimate tyre degradation for each compound, providing an additional input for the strategy prediction process.

**Data**

Huge variety of data has been used during the project. Some of them are directly coming from Open F1 API and some of them are engineered and derived from Open F1 data. For further info and details, please check the notebooks. The models are trained on and require the following data inputs: 

1. **Starting Compound prediction model**

- `location`: dThe location (city) of the grand prix
- `avg_track_temperature`: Average Temperature of the track when race starts
- `track_length`: The lengths of the track in meters
- `n_of_corners`: How many corners the given track has
- `degradation`: The level of degradation of the given track
- `overtake_difficulty`: How difficult it is to perform an overtake
- `avg_pit_time`: What is the average pit loss in seconds
- `driver_number`: The number of the driver
- `full_name`: The full name of the driver
- `team_name`: The driver's team
- `grid_category`: Which is the grid category: Top-field, Mid-field, Back-field
- `dist_hard`: The distribution of the grid-category using hard compound
- `dist_medium`: The distribution of the grid-category using medium compound
- `dist_soft`: The distribution of the grid-category using soft compound
- `driver_baseline_pace`: The average baseline pace of the given driver by circuit
- `grid_position`: The starting grid position of the given driver

2. **Determining first stint model**

- `location`: The location (city) of the grand prix
- `avg_track_temperature`: Average Temperature of the track when race starts
- `track_length`: The lengths of the track in meters
- `n_of_corners`: How many corners the given track has
- `degradation`: The level of degradation of the given track
- `overtake_difficulty`: How difficult it is to perform an overtake
- `tipical_n_of_pitstops`: The usual number of pit stops on a given grand prix
- `avg_pit_time`: What is the average pit loss in seconds
- `driver_number`:The number of the driver
- `full_name`: The full name of the driver
- `team_name`: The driver's team
- `grid_category`: Which is the grid category: Top-field, Mid-field, Back-field
- `starting_compound`: The starting tyre compound used by the driver (the previous model predicts it)
- `driver_baseline_pace`: The average baseline pace of the given driver by circuit
- `grid_position`:The starting grid position of the given driver
- `tyre_age_at_start`: The age of the tyres at start. e.g 0 or 2
- `avg_hard_stint_by_race`: The average length of stints performed on a given race on hard
- `avg_med_stint_by_race`: The average length of stints performed on a given race on medium
- `avg_soft_stint_by_race`: The average length of stints performed on a given race on soft
- `avg_hard_stint_by_driver`: The average length of stints performed on a given race by driver on hard
- `avg_med_stint_by_driver`: The average length of stints performed on a given race by driver on medium
- `avg_soft_stint_by_driver`:The average length of stints performed on a given race by driver on soft

## Model Evaluation 

*Note*: The dataset is relatively limited, containing only three years of starting grid data. As more historical data is collected over time, the models' predictive accuracy is expected to improve.

### 1. Starting Compound prediction model

The model exhibits a bias toward selecting the `MEDIUM` compound, likely reflecting historical trends in which it was the predominant starting choice. As demonstrated in the EDA notebook across all position groups (Top-row, Top-ten, and Second-half), the MEDIUM compound consistently emerges as the overwhelmingly preferred option.

![compound distribution](imgs/compound_distribution.png)

herefore, the model's strongest performance in identifying the `MEDIUM` compound is consistent with the observed historical trends. Although its predictive accuracy for the `HARD` and `SOFT` compounds is comparatively lower, its overall performance remains acceptable. As additional data becomes available, the model's predictive capabilities could be further improved through continued training and refinement.

The model is evaluated based on the following metrics: 

**F1-Score by compound**

The F1-score represents the harmonic mean of precision and recall, providing a single metric that balances both measures.

It is quite visible that MEDIUM has the best F1 score. 

![F1 score](imgs/F1_score_by_compound.png)

**Multiclass PR-Curve**

The Precision–Recall (PR) curve visualizes the trade-off between **precision** and **recall** across varying classification thresholds. This metric is particularly informative when dealing with **imbalanced datasets**, where the positive class occurs much less frequently than the negative class. In this case this is not the best metric. The ROC-Curve is more informative.

- **Precision** measures the proportion of predicted positives that are actually correct.  
- **Recall** measures the proportion of actual positives that are correctly identified.

A higher area under the PR curve indicates a model that maintains strong precision while achieving high recall.

As visible on the plot, the `MEDIUM` compound has the best PR score, because overall it has the best Average Precision, which is not surprising considering the fact that the majority of the samples are `MEDIUM` compounds. 

![PR Curve](imgs/Multiclass_PR_CURVE.png)

**Multiclass ROC-Curve**

The Receiver Operating Characteristic (ROC) curve illustrates the model’s ability to distinguish between classes across different classification thresholds. It plots:

- **True Positive Rate (Sensitivity / Recall)** on the y-axis  
- **False Positive Rate** on the x-axis  

A model with strong discriminative ability will produce a curve that approaches the top-left corner of the plot. The ROC curve is commonly summarized using the **Area Under the Curve (AUC)**, where higher values indicate better overall classification performance.

The plot proves that the model performs better on all compounds than random guessing.

![ROC Curve](imgs/MultiClass_ROC_CURVE.png)

**Confusion Matrix**

The confusion matrix summarizes the classification results by comparing the predicted labels with the true labels. It provides a detailed breakdown of:

- **True Positives (TP)** – correctly predicted positive instances  
- **True Negatives (TN)** – correctly predicted negative instances  
- **False Positives (FP)** – negative instances incorrectly classified as positive  
- **False Negatives (FN)** – positive instances incorrectly classified as negative 

As shown below, the model predicts the `MEDIUM` compound with relatively high accuracy, largely due to its overrepresentation in the dataset. However, it tends to misclassify `HARD` and `SOFT` compounds as `MEDIUM` more frequently than desired.

Several approaches could help improve the model's performance. First, expanding the training dataset would likely enhance its predictive accuracy, as the current model is trained on only approximately 1,700 rows of data, which is relatively limited for a robust predictive model. However, this limitation reflects the amount of data available for the analysis. Additionally, engineering new features and incorporating relevant data from external sources could provide further insights and improve the model's ability to distinguish between the three compound types.

![Confusion Matrix](imgs/Confusion_matrix.png)

**Other Metrics**

![other scores](imgs/XGboost_scores.png)

  
### 2. First Stint prediction model