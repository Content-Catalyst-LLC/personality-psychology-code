# Methods

This directory supports a small reproducible analysis of personality and creativity outcomes.

## Conceptual model

The article argues that creativity should be treated as a plural construct. The workflows therefore separate:

1. divergent thinking;
2. creative achievement;
3. everyday creativity.

The central model can be written as:

\[
C_i = \alpha + \beta_1 O_i + \beta_2 D_i + \beta_3 E_i + \beta_4 S_i + \varepsilon_i
\]

where:

- \(C_i\) is a creative outcome;
- \(O_i\) is openness or openness-related disposition;
- \(D_i\) is domain knowledge or domain context;
- \(E_i\) is execution/persistence capacity;
- \(S_i\) is social support or opportunity.

## Analytic strategy

The Python and R scripts run:

- descriptive summaries;
- correlation matrices;
- ordinary least squares models;
- domain-sensitive models using categorical predictors;
- output tables and figures.

## Interpretation

The analysis should be read as a transparent demonstration of model logic. It does not estimate real psychological effect sizes.
