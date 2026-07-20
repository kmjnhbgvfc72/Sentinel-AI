# Risk Prediction

Path risk combines event risk score (55%), AI confidence (20%), target criticality (15%), and an explicit high/critical vulnerability uplift. Asset risk combines event exposure (45%), asset criticality (30%), historical incident weight (15%), and vulnerability uplift. Scores are clamped to 0–100 and mapped to low, medium, high, or critical. A small trained Random Forest adjustment can be applied to path length and event risk; absent trusted artifacts, the deterministic base remains active.
