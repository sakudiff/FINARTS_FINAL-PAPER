# Disclosure Blocks for QMD Code Chunks

Each block follows the same skeleton: (AND) what the paper says, (BUT) what it does not say, (THEREFORE) what we decide and why. No hedging. No semicolons. No em dashes. No bold labels.

---

## Block 1: VAR Setup (data loading, period filtering, exogenous dummies)

Beirne and Sugandi state they include a time dummy and seasonal dummies as exogenous variables in every VAR specification. They do not disclose the structure of either. The seasonal dummies are described only as "seasonal dummies," without specifying monthly, quarterly, or any other periodicity. The time dummy is mentioned but not defined as a linear trend, a break dummy, or an intercept shift.

Our specification uses eleven monthly indicator variables with January as the reference month and a linear time trend indexed 1 through T. The monthly structure is the natural reading of "seasonal dummies" in a daily-frequency VAR where the lower-frequency inputs (WUI, REER, RGDP, capital flows) are interpolated from monthly or quarterly source data. The interpolation itself injects artificial intra-period variation that monthly indicators absorb, preventing the seasonal pattern in the source data from biasing coefficient estimates. The linear trend is the simplest time dummy that satisfies the paper's stated requirement.

This is an estimation of what the authors did, not a replication of a disclosed choice. The paper provides no evidence to contradict monthly dummies over quarterly, and monthly is the more conservative choice because it captures more seasonal structure than the authors could have needed.

---

## Block 2: Stationarity Tests (ADF)

Beirne and Sugandi state that "all endogenous variables are stationary." They do not report which test they used, what lag structure they specified for the test, what significance threshold they applied, or whether they tested in levels or differences. The claim is asserted without evidence.

We apply the Augmented Dickey-Fuller test to each of the ten transformed variables exactly as they enter the VAR. The test includes a constant term. Lag length is selected by AIC with a maximum of 20 lags to match the VAR lag search. The significance threshold is 5%, consistent with the 95% confidence intervals reported throughout the paper.

This decision is defensible because the ADF test with AIC-based lag selection is the standard stationarity test in the VAR literature. The 5% threshold matches the paper's stated confidence level. If a variable tests as non-stationary, we flag it and report the result without differencing, because the paper asserts stationarity and we preserve their specification. The discrepancy, if it arises, is a finding worth reporting.

---

## Block 3: Lag Selection (AIC Search)

Beirne and Sugandi state that the optimum lag k is chosen by the Akaike Information Criterion. They do not state the maximum lag they searched. For a ten-variable VAR on daily data, the number of coefficients grows as 10 squared times k, so the choice of max lag directly constrains the search space and therefore the selected model.

We search lags 1 through 20. This range is generous enough to capture monthly effects (approximately 22 trading days) and quarterly effects (approximately 66 trading days) while keeping the parameter count within a range that daily data can support. At lag 20, each equation estimates 200 coefficients from the endogenous variables plus 12 coefficients from the exogenous variables. With 5,795 observations in the replication period, the observation-to-parameter ratio exceeds 28 to 1, which is adequate for AIC to discriminate without overfitting.

The paper does not disclose their max lag. Our range of 20 exceeds what the published literature typically searches for monthly VARs (8 to 12 lags) and is calibrated to daily frequency where shorter lags capture the high-frequency dynamics that matter for risk-off shocks. If the AIC selects a lag at the upper bound of our search range, we flag this as a potential indication that the true optimum lies beyond 20.

---

## Block 4: Restricted VAR Estimation

Beirne and Sugandi describe the block exogeneity restriction precisely. The Risk-off variable is affected only by its own lagged values. The other nine endogenous variables are affected by each other's lagged values and by the lagged values of Risk-off. The restriction is implemented by setting the coefficients on all non-Risk-off variables to zero in the Risk-off equation.

The paper does not disclose the software package or estimation method used.

We implement the restriction using `statsmodels.tsa.var_model.VAR.fit_constrained()`, which enforces zero constraints during the maximum likelihood optimization. The constraint matrix zeros out all coefficients on WUI, Spread, RGDP, REER, Stock Index, Debtsec, Equity, Other, and Direct across all lags in the Risk-off equation. Coefficients on the exogenous variables (seasonal dummies, time trend) are not constrained, which matches the paper's specification.

If `fit_constrained()` fails due to singularity or convergence failure, we fall back to manual ordinary least squares: the Risk-off equation is estimated separately on its own lags and the exogenous variables, and the remaining nine equations are estimated jointly with Risk-off lags included. The fallback preserves the block exogeneity structure while using a more numerically stable estimator.

This is a replication of a clearly disclosed restriction using a software implementation that matches the paper's stated mathematical specification.

---

## Block 5: Unrestricted VAR Estimation

Beirne and Sugandi state that in the unrestricted VAR, "each endogenous variable in the model is affected by the lagged values of itself and other endogenous variables." This is the standard VAR definition. No restriction is applied.

We estimate the unrestricted VAR using `statsmodels.tsa.var_model.VAR.fit()` with the lag selected by AIC in Block 3. No constraints are imposed on any coefficient. The exogenous variables (seasonal dummies, time trend) enter every equation.

This is a direct replication of a clearly disclosed specification. No estimation is required.

---

## Block 6: Impulse Response Functions with Analytical Confidence Intervals

Beirne and Sugandi report impulse responses to a one-standard-deviation structural shock on the Risk-off variable. They use a Cholesky identification scheme with the ten-variable ordering specified in Section 4 of the paper. The horizon is 125 days, confirmed by the x-axis limits in Figures 4 through 10. They state that "95% confidence intervals are provided by the dotted lines." They do not disclose the method used to compute those confidence intervals.

We compute the IRFs using the Cholesky decomposition implied by the paper's variable ordering, with Risk-off as the most exogenous variable and Direct as the most endogenous. The shock size is one standard deviation of the Risk-off innovation. The horizon is 125 working days.

The confidence intervals are computed using the analytical (asymptotic normal) approximation, which is the default in every major VAR software package and the most likely method the paper used. The analytical method assumes normally distributed residuals. We know from the descriptive statistics that `other_pct` is right-skewed (mean 0.39, maximum 28.55, standard deviation 3.16) and that `risk_off` is binary. The normality assumption is violated. Nonetheless, the analytical method is the standard in the published VAR literature and is what the paper almost certainly used, because no paper that bootstraps or simulates its CIs fails to mention it.

---

## Block 7: Impulse Response Functions with Bootstrap Confidence Intervals

This block is not a replication of anything in the paper. The paper does not mention bootstrap, Monte Carlo simulation, or any non-analytical confidence interval method. This is an extension we add as a robustness check.

The justification is structural, not speculative. The capital flow variables in our dataset exhibit non-normal distributions. `other_pct` has a skewness implied by its mean (0.55) being far from its midpoint, and the binary `risk_off` variable cannot produce normally distributed residuals by construction. The analytical CIs assume normality and therefore understate uncertainty in the tails. Bootstrap CIs make no distributional assumption and provide a more honest assessment of sampling variability.

We implement residual-based bootstrap with 1,000 replications. Each replication resamples the VAR residuals with replacement, generates a new set of endogenous variables by feeding the resampled residuals through the estimated coefficient matrices, re-estimates the VAR, and recomputes the IRFs. The 2.5th and 97.5th percentiles across replications form the 95% confidence band.

If the bootstrap CIs are wider than the analytical CIs, the difference measures the cost of the normality assumption. If they are narrower, the analytical method was conservative. Both outcomes are informative.

---

## Block 8: IRF Comparison (Restricted vs Unrestricted, Analytical vs Bootstrap, Replication vs Extended)

This block has no corresponding section in the paper. It is a synthetic output that aggregates the four model estimates (restricted and unrestricted, each on two periods) and two CI methods for comparison.

The comparison serves a specific forensic purpose. The paper reports IRFs for the restricted model only in its main figures (Figures 4 through 10) and defers unrestricted results to the appendix. By plotting both side by side, we can assess whether the block exogeneity restriction materially changes the impulse responses. If the restricted and unrestricted IRFs are similar, the restriction is harmless and the reported results are robust. If they diverge, the restriction is driving the findings.

The period comparison (1999 to 2021 versus 1999 to 2026) tests whether the yen's safe haven properties survive the 2022 to 2026 period, which includes the Bank of Japan's yield curve control exit, the August 2024 carry trade unwind, and the Iran conflict risk-off episode. If the extended-period IRFs differ from the replication-period IRFs, the structural relationship has shifted. We overlay the two IRF traces on the same axes and mark the difference.

---

## Block 9: Forecast Error Variance Decomposition

The working paper version of Beirne and Sugandi (ADBI Working Paper 1345) does not mention forecast error variance decomposition. The published Pacific-Basin Finance Journal version may include it. We include FEVD as a standard VAR diagnostic because it answers a question the IRFs leave open: how much of the Risk-off shock's total effect on each variable is attributable to the shock itself versus propagation through the system.

We compute the FEVD at the same 125-day horizon as the IRFs. The decomposition uses the same Cholesky ordering, so the variance allocation inherits the same identification assumptions. We report the fraction of forecast error variance explained by the Risk-off shock for each variable at horizons of 1, 5, 20, 60, and 125 working days. The tabular format allows direct comparison across variables and periods.

The tables also serve as a consistency check. If the Risk-off shock explains essentially zero variance in variables where the paper found significant IRFs (such as REER), the Cholesky ordering may be suppressing the effect rather than identifying it. This is a diagnostic limitation worth reporting.
