# 📞 Bank Marketing (Term Deposit Subscription) Dataset  
**Source :** [UCI Machine Learning Repository – Bank Marketing (#222)](https://archive.ics.uci.edu/dataset/222/bank+marketing)  

> A Portuguese retail bank’s phone-based marketing campaigns (May 2008 → Nov 2010).  
> The task is to **predict whether a client will subscribe to a term deposit** (target `y`).

---

## 1 · Background  

- Each row records the outcome of the **last phone call** (plus client history).  
- Multiple calls to the **same client** may appear across campaigns.  
- The original authors showed that **data-driven targeting** boosts campaign ROI – see the reference paper below.

---

## 2 · Files in this Kaggle release  

| File | Rows | Columns | Notes |
|------|------|---------|-------|
| `bank_marketing.xlsx` | **45 211** | **17** | Classic **“bank-full”** version (all examples, 17 predictors + target) |

> *Need the enriched “bank-additional” version with 20 predictors? Grab it from the UCI link.*

---

## 3 · Data Dictionary (17 predictors + target)

| Column | Type | Description |
|--------|------|-------------|
| `age` | int | Age of the client |
| `job` | cat | Job type (admin., blue-collar, …) |
| `marital` | cat | Marital status (married / single / divorced) |
| `education` | cat | Education level (primary / secondary / tertiary / unknown) |
| `default` | bin | Has credit in default? |
| `balance` | int | Average yearly balance (EUR) |
| `housing` | bin | Has housing loan? |
| `loan` | bin | Has personal loan? |
| `contact` | cat | Contact channel (cellular / telephone / unknown) |
| `day` | int | Day of month of last contact |
| `month` | cat | Month of last contact (`jan`-`dec`) |
| `duration` | int | Call duration (secs)\* |
| `campaign` | int | Contacts made in this campaign (incl. last) |
| `pdays` | int | Days since last contact (-1 ⇒ never) |
| `previous` | int | Previous contacts before this campaign |
| `poutcome` | cat | Outcome of previous campaign (failure / success / nonexistent) |
| **`y`** | bin | **Target** – subscribed to term deposit? (`yes`/`no`) |

\*⚠️ `duration` is only known *after* the call ends; include it **only for benchmarking**, not for live prediction.

---

## 4 · Quick Start in Python  

```python
import pandas as pd

df = pd.read_excel('/kaggle/input/bank-marketing/bank_marketing.xlsx')
print(df.shape)          # (45211, 17)
df.head()

Prefer pip? Fetch directly from ucimlrepo:
'''
!pip install ucimlrepo
from ucimlrepo import fetch_ucirepo
bm = fetch_ucirepo(id=222)
X, y = bm.data.features, bm.data.targets
'''

## 5 · Use-Cases & Ideas  

| 🛠️ ML Task              | Why it’s interesting                                                                                           |
|--------------------------|----------------------------------------------------------------------------------------------------------------|
| Binary classification    | Classic imbalanced dataset – try **SMOTE**, cost-sensitive learning, threshold tuning                         |
| Feature engineering      | Combine `pdays`, `campaign`, `previous` into a **contact-intensity score**                                     |
| Model interpretability   | Use **SHAP** / **LIME** to explain “yes” predictions                                                           |
| Time-aware validation    | Data are date-ordered → split train/test chronologically to avoid leakage                                      |

---

## 6 · Credits & Citations  

> **Creators :** **Sérgio Moro, Paulo Rita, Paulo Cortez**  
> **Original paper :**  
> Moro S., Cortez P., Rita P. (2014).  
> *A data-driven approach to predict the success of bank telemarketing campaigns.*  
> *Decision Support Systems.* [[PDF]](https://www.semanticscholar.org/paper/cab86052882d126d43f72108c6cb41b295cc8a9e)

If you use this dataset, please cite:

Moro, S., Rita, P., & Cortez, P. (2014). Bank Marketing [Dataset].
UCI Machine Learning Repository. https://doi.org/10.24432/C5K306


---

## 7 · License  

This dataset is released under the **Creative Commons Attribution 4.0 International (CC BY 4.0)**.  
You are free to share & adapt, **provided you credit the original creators**.


