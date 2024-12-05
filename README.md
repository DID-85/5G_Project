# **AI/ML for 5G Network Optimization**

## **Introduction**
This project addresses the critical challenge of energy consumption in 5G networks, specifically in **Base Stations (BSs)**, which account for over 70% of the total energy usage. Using advanced **Artificial Intelligence (AI)** and **Machine Learning (ML)** techniques, this project aims to optimize energy utilization while maintaining service quality.

The solution integrates a **Hybrid-Boosted Ensemble Model** with a **Mixture of Experts (MoE)** architecture to predict and generalize energy consumption across different scenarios, including cold-start configurations.

---

## **Features**
- Accurate energy consumption predictions for 5G base stations.
- Generalization across diverse base station configurations.
- Robust handling of scenarios with no historical traffic data.
- Significant improvements in prediction accuracy using a hybrid-boosted model.

---

## **Objectives**
1. **Energy Prediction**: Estimate energy consumption for specific base stations based on historical data.
2. **Generalization**: Extend predictions to new base station configurations using hardware attributes.
3. **Cold Start Scenarios**: Handle cases where historical data is unavailable, relying solely on configuration parameters.

---

## **Project Structure**

```plaintext
├── data/
│   ├── base_station_config.csv        # Base station configuration details
│   ├── traffic_stats.csv              # Hourly traffic statistics
│   ├── energy_consumption.csv         # Energy consumption data
├── models/
│   ├── ridge_regression.py            # Ridge regression implementation
│   ├── xgboost_model.py               # XGBoost implementation
│   ├── hybrid_model.py                # Hybrid-boosted ensemble model
├── notebooks/
│   ├── 5G_Optimization.ipynb          # Jupyter notebook with full workflow
├── results/
│   ├── performance_metrics.csv        # Model evaluation metrics
│   ├── visualizations/                # Graphs and plots
├── README.md                          # Project documentation
└── requirements.txt                   # Python dependencies
```
## ** Methodology**Methodology
1. Dataset Overview
The dataset consists of:

Base Station Configurations: Attributes like frequency, antennas, TX power.
Traffic Statistics: Hourly load metrics and energy-saving mode activations.
Energy Consumption Data: Hourly energy usage measurements.
2. Feature Engineering
Temporal Features: Lag variables, differences, and seasonality patterns.
Polynomial Features: Non-linear transformations for configuration data.
Clustering: k-means applied to base station configurations for generalization.
3. Model Architecture
The Hybrid-Boosted Ensemble Model comprises:

Ridge Regression: For capturing linear trends in the data.
XGBoost: To model non-linear relationships and residuals.**
Mixture of Experts (MoE): Routes data to specific expert models (A, B, C) based on characteristics.
**Results
Model Performance:
WMAPE: 6.99% on the private leaderboard.
**31.94% improvement over baseline models.
Comparison:
Ridge Regression: Moderate accuracy, good extrapolation.
XGBoost: High accuracy, limited generalization.
Hybrid Model: Best overall performance, combining strengths of both.
Model	CV Final (WMAPE)	Private LB
Only Ridge Regression	8.37%	9.55%
Only XGBoost	5.73%	9.68%
Hybrid-Boosted Model	5.72%	6.99%
**Installation
Clone the repository:

bash
Copy code :
git clone (https://github.com/DID-85/5G_Project/tree/main).git
**cd 5g-optimization
**Install dependencies:

bash
Copy code :
pip install -r requirements.txt
**Run the Jupyter notebook:

bash
Copy code
jupyter notebook notebooks/5G_Optimization.ipynb
**Usage
Data Preprocessing:

Normalize continuous features like Load and Energy.
Engineer lag variables and clusters.
**Model Training:

Run hybrid_model.py to train the hybrid-boosted ensemble model.
bash
Copy code
python models/hybrid_model.py
**Evaluation:

View performance metrics in results/performance_metrics.csv.
Visualization:

**Graphs and plots in results/visualizations/ for better insights.
**Key Achievements
Improved energy consumption prediction accuracy by 31.94%.
Developed a scalable model adaptable to new and dynamic 5G scenarios.
Aligned with Sustainable Development Goals (SDGs) by minimizing the energy footprint of 5G networks.
**Future Work
Replace ridge regression with neural networks for enhanced extrapolation.
Implement real-time predictions for live traffic scenarios.
Explore adaptive masks to dynamically refine model predictions.


**License
This project is licensed under the MIT License. See LICENSE for details.
