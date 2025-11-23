
# 🏥 Lifestyle & Health Analytics Dashboard

**CEN445 – Introduction to Data Visualization**

## 📌 **1. Project Overview**

This project presents an interactive **Lifestyle & Health Analytics Dashboard** built using **Streamlit**.
The goal is to explore **how lifestyle behaviors (smoking, alcohol, exercise, sleep)** relate to **health outcomes, BMI, sleep patterns, and country-level lifestyle differences**.

The dashboard integrates **nine advanced data visualizations**, a **3D Network Diagram**, and a **Machine Learning Classification Model** predicting **Health Risk**.

The dataset used:
🔗 *Lifestyle and Health Risk Prediction Dataset*
[https://www.kaggle.com/datasets/miadul/lifestyle-and-health-risk-prediction](https://www.kaggle.com/datasets/miadul/lifestyle-and-health-risk-prediction)



## 📌 **2. Dataset**

The dataset includes a combination of categorical and numerical variables such as:

* **Demographics:** age, profession, marital status, country
* **Lifestyle Indicators:** smoking, alcohol use, exercise frequency, sugar intake
* **Health Metrics:** BMI, sleep duration, health risk

This dataset is suitable because it contains **multi-dimensional lifestyle and health-related features**, allowing rich visualization and modeling.


## 📌 **3. Dashboard Features**

The application is fully interactive and includes:

### ✔️ **Dynamic Sidebar Filters**

Users can filter by:

* Age group
* Profession
* Marital status
* Exercise frequency
* Sugar intake
* Sleep range
* Weight, height, BMI
* Lifestyle habit category
* Country (for geo visualization)

All visualizations update dynamically when filters change.


## 📌 **4. Visualizations**

###**🔶 4.1 Stacked Bar Chart — Alcohol & Smoking Across Age Groups**

Visualizes the distribution of alcohol and smoking habits across different age groups. The overall pattern is clear: in every age range, the “None” category (individuals who do not smoke or drink) dominates.

💡Insight:
 * Individuals with no harmful habits form the largest group across all age categories.
 * The Alcohol Only and Smoking Only categories remain consistently low, with slight variations by age.
 * The Both (Smoking & Alcohol) category shows the lowest prevalence in all age groups.
 * Alcohol consumption appears slightly higher among ages 18–25 and 56–65 compared to other groups.

### **🔶 4.2 Treemap — Sugar Intake vs Exercise → BMI**

Displays BMI variation across combined lifestyle patterns.

💡Insight:
 * Sugar intake alone does not drastically change BMI.*
 * Exercise frequency is a much stronger determinant.*

### **🔶 4.3 Heatmap — Sleep vs Smoking/Alcohol Habits**

Illustrates how smoking and alcohol behaviors impact average sleep duration across different age ranges.This visualization highlights that lifestyle habits can affect sleep patterns in unexpected ways — especially the combination of smoking + alcohol, which correlates with increased sleep in certain age ranges

💡Insight:
 * Individuals who engage in both smoking and alcohol consumption show the highest average sleep durations, especially in the 26–35 and 36–45 age groups.
 * The Smoking Only and Alcohol Only categories display similar sleep levels, without major differences.
 * The None group maintains a more stable and balanced sleep pattern across all ages.
 * Sleep duration tends to slightly increase with age, particularly in the 66–80 age group.

### **🔶 4.4 Effect of Age and BMI on Health Risk — Sankey Diagram**

Visualizes how age groups and BMI categories independently contribute to overall health risk levels.Age and BMI act as two separate sources feeding into the same health-risk node, allowing us to clearly observe how each factor influences the outcome.

💡Insights:
 * Health risk increases significantly with age, especially among individuals aged 46 and above, who predominantly flow into the High Risk category.
 * Higher BMI strongly correlates with higher health risk; flows from Overweight and Obese groups are heavily concentrated in the High Risk segment.
 * The Low Risk group is mostly composed of younger individuals (18–35) and those with Normal BMI.Underweight and Normal BMI categories mostly flow toward Low Risk.

### **🔶 4.5 Geometric Map — Lifestyle Score by Country**

Displays the average Lifestyle Score and High Health Risk Rate for each country. It allows users to compare lifestyle habits—such as exercise level, sleep duration, and sugar intake—across different regions.When hovering over a country, additional details are shown, including average lifestyle metrics and the number of participants from that region.

💡Insights:
 * Countries with healthier lifestyle behaviors tend to have lower health risk levels.
 * Countries with poor lifestyle habits typically show a higher proportion of high-risk individuals.


### **🔶 4.6 Histogram — BMI Distribution**

Shows BMI distribution across the population.

💡Insights:
 * Most individuals fall between **20–30 BMI**, showing a near-normal distribution.

### **🔶 4.7 Swarm Plot — BMI vs Lifestyle Habit Category**

Shows granular BMI distribution points.

💡Insights:
 * Heavy lifestyle habits (smoking+alcohol) → slightly higher BMI spread.

### **🔶 4.8 Violin Plot — BMI Distribution by Age Group**

Shows KDE + boxplot across age categories.

💡Insights:
 * Older age groups have wider BMI spread and higher median BMI.

### **🔶 4.9 3D Network Diagram — Lifestyle → Sleep → Health Risk**

This updated network visualizes **causal proximity** between:

* Smoking
* Alcohol
* Exercise
* Sleep duration (clustered groups)
* Health Risk categories

💡Insight:
 * Sleep acts as a **bridge node** between lifestyle behaviors and health risk.
 * Smoking/alcohol cluster away from the “Low Risk” nodes.
 * Balanced sleep group connects more strongly to “Low Risk”.

This graph explains **combined lifestyle effects**, not isolated ones.


## 📌 ** 5.Machine Learning Model — Health Risk Classification**

 **Random Forest Classifier** predicts health risk levels:

* **Low**
* **Medium**
* **High**

Features used:

* Age
* BMI
* Sleep duration
* Exercise frequency
* Smoking
* Alcohol

User inputs values, presses **“Predict”**, and receives:

* **Health Risk result**
* Color-coded interpretation
* Model accuracy

Insight:
🔍 BMI, age, and smoking/alcohol behaviors are major predictors.


## 📌 **6. What we Learned **

From this project, I observed that:

* **Exercise has a stronger effect on BMI** than sugar intake.
* **Age and BMI are the primary drivers of health risk.**
* Excessive sugar intake alone does **not** significantly change BMI.
* Surprisingly, **some smokers/drinkers sleep more** than expected.
* Lifestyle patterns are multi-dimensional and should not be analyzed independently.

This dashboard helped me understand **which lifestyle behaviors truly matter** and how they connect to health outcomes.

## 📌 **7. Technical Architecture**

### ✔️ **Frontend**

* Streamlit
* Plotly

### ✔️ **Backend + Processing**

* Pandas
* NumPy
* scikit-learn
* NetworkX

### ✔️ **ML Model**

* RandomForestClassifier
* Label Encoding
* Balanced three-class mapping (Low / Medium / High)

### ✔️ **Modules Structure**

```
charts/
   stacked_bar.py
   treemap.py
   heatmap.py
   multi_sankey.py
   geo_map.py
   histogram.py
   network_diagram.py
   swarm.py
   violin_plot.py

ml_model.py
app.py
README.md
```

---

## 📌 **8. How to Run the Project**

### **Install Requirements**

```
pip install -r requirements.txt
```

### **Run the App**

```
streamlit run app.py
```

---

## 📌 **9. Team Contributions**

### **Özlem Tay**

* Sidebar filtering system
* Stacked Bar, Heatmap, Treemap
* Sankey Diagram
* Integrations & UI
* Network diagram modifications
* ML Classification Model
* Full dashboard assembly

### **Işıl Nur Taşdemir**

* Histogram
* Swarm Plot
* Violin Plot
* Geographic diagram
* Original network diagram structure

### **Zeynep Vurucu**

* Map refinement
* Geographic diagram modification
* Data cleaning and feature improvements

## 📌 **10. Team members**

### **Özlem Tay  ID:2022555467**
### **Işıl Nur Taşdemir ID:2018556064**
### **Zeynep Vurucu ID:2019555462**


