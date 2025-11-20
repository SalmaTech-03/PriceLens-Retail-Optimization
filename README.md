
# 🏷️ PriceLens: Retail Pricing & Demand Optimization Engine

<!-- TECH STACK BADGES -->
<div align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Power_BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black" />
  <img src="https://img.shields.io/badge/SciPy-8CAAE6?style=for-the-badge&logo=scipy&logoColor=white" />
  <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" />
  <img src="https://img.shields.io/badge/StatsModels-E32F2F?style=for-the-badge&logo=python&logoColor=white" />
</div>

<div align="center">
  <strong>🤖 AI-Driven • 📉 Elasticity Modeling • 💰 Profit Maximization</strong>
</div>

<br />


---

## 🚀 Executive Summary

**PriceLens** is an algorithmic pricing intelligence engine designed to solve the retail "Margin vs. Volume" trade-off. 

Traditional retail pricing often relies on static rules (e.g., "Cost + 20%"). PriceLens moves beyond this by using **econometric machine learning** to estimate price elasticity for **50+ SKUs** and creates a mathematical optimization loop to recommend the exact price point that maximizes daily gross profit.

### 🏆 Key Business Outcomes (Simulation)
| Metric | Impact | Description |
| :--- | :--- | :--- |
| **Profit Uplift** | **+7.5%** | Identified ~$700/day in lost margin opportunity. |
| **Strategy** | **Granular** | Differentiated pricing for "Cash Cows" vs "Traffic Drivers". |
| **Automation** | **100%** | End-to-end pipeline from Raw Data → Optimization → BI Dashboard. |

---

## 🧠 The Science: Econometrics & Optimization

PriceLens uses a two-step mathematical approach to ensure recommendations are robust and data-driven.

### 1. Demand Estimation (Log-Log Regression)
We utilize `statsmodels` to fit a Log-Log regression model. This allows us to interpret coefficients directly as **Price Elasticity**.

$$ \ln(\text{Quantity}) = \beta_0 + \beta_1 \ln(\text{Price}_{\text{own}}) + \beta_2 \ln(\text{Price}_{\text{comp}}) + \text{Seasonality} + \epsilon $$

*   $\beta_1$: **Own-Price Elasticity** (How sensitive customers are to price changes).
*   $\beta_2$: **Cross-Price Elasticity** (Cannibalization effect from competitors).

### 2. Non-Linear Optimization
We define a profit function and use `scipy.optimize` (L-BFGS-B algorithm) to find the global maximum for every SKU, subject to business constraints (e.g., price cannot exceed competitor by >20%).

$$ \text{Maximize } \pi(P) = (P - \text{Cost}) \times e^{(\beta_0 + \beta_1 \ln(P) + \dots)} $$

---

## 📂 Project Architecture

The project is structured as a production-ready pipeline:

```bash
PriceLens/
├── 📂 data/
│   ├── 📄 raw/                  # Synthetic enterprise transactions (generated)
│   └── 📄 processed/            # Cleaned modeling data
├── 📂 src/
│   ├── 📂 econometrics/         # Elasticity modeling logic (OLS/Mixed Effects)
│   ├── 📂 optimization/         # SciPy solver for profit maximization
│   └── 📂 utils/                # Data generators & helpers
├── 📂 reports/                  # Power BI Dashboard (.pbix) & Assets
├── 🐍 main_pipeline.py          # Execution Entry Point
└── 📄 requirements.txt          # Dependencies
```

---

## 📊 Dashboard Capabilities

The interactive **Power BI Dashboard** allows Category Managers to interpret the complex math through simple visuals:

*   **Strategy Matrix (Scatter Plot):** Plots *Elasticity* vs. *Profit Potential*.
    *   *Top Left:* **Cash Cows** (Inelastic & High Margin) → **Action: Raise Price**.
    *   *Bottom Right:* **Risky Items** (Highly Elastic) → **Action: Discount/Hold**.
*   **Scenario Simulator:** A "What-If" analysis tool to see how price changes impact total revenue.
*   **Action List:** Prioritized table of SKUs requiring immediate price updates.

---

## 💻 How to Run

1. **Clone the Repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/PriceLens-Retail-Optimization.git
   cd PriceLens-Retail-Optimization
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Pipeline** (Generates Data -> Trains Model -> Optimizes Prices)
   ```bash
   python main_pipeline.py
   ```

---

<div align="center">
  <p><i>Built with ❤️ using Python & Power BI</i></p>
</div>
```
