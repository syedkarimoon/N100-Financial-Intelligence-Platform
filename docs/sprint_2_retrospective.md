# Sprint 2 Retrospective — Financial Intelligence Engine

## Completed Modules

- Financial ratio engine
- CAGR engine
- Growth scoring engine
- Composite quality score
- Ratio edge case validation


## Formula Decisions

### Revenue CAGR

Formula:

Ending Value / Beginning Value ^ (1/n) - 1


### PAT CAGR

Used net profit growth over 5 year period.


### EPS CAGR

Used EPS growth over 5 year period.


### ROE

Analytics uses:
financial_ratios.return_on_equity_pct

Source roe_percentage is used only for display.


### Debt Equity

Financial sector companies excluded from D/E warning because leverage is structurally normal.


## Edge Case Resolutions

### ROE anomalies

Category:
Data source issue

Reason:
Source company-level ROE values differ from yearly calculated ROE.


### TCS ROE anomaly

Source:
0.52

Decision:
Use calculated ratio engine value.


### ROCE

Category:
Version difference

Reason:
Source ROCE exists, calculated ROCE engine pending.


## Screener Validation

Filter:

ROE > 15%
Debt Equity < 1

Latest year records used.

Result:

41 companies passed.