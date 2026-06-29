---
layout: page
title: Does Studying More Raise GPA? A Causal-Inference Workflow
description: A plain regression says studying lowers GPA. Here's why that's wrong, and how matching gets closer to the real answer.
img: assets/img/causal_dag.svg
importance: 6
category: work
---

Does studying more actually raise your GPA? On this [student dataset](https://www.kaggle.com/datasets/nabilajahan/student-study-performance/data), a plain regression says no. It finds that more study hours go with a *lower* GPA.

<div class="row justify-content-center mt-3">
    <div class="col-sm-10">
        {% include figure.liquid loading="eager" path="assets/img/causal_backwards_result.svg" title="Expected vs. naive regression result" class="img-fluid" %}
    </div>
</div>
<div class="caption">
    The regression coefficient on study hours comes out negative and significant. That answer is almost certainly backwards.
</div>

---

### Why the regression is wrong: confounding

Things like sleep, motivation, and ability affect both how much a student studies *and* the GPA they end up with. A struggling student may study more precisely because they're behind. A plain regression can't separate that tangle from the real effect, so the number it reports is biased.

<div class="row justify-content-center mt-3">
    <div class="col-sm-10">
        {% include figure.liquid loading="eager" path="assets/img/causal_dag.svg" title="Confounding between study hours and GPA" class="img-fluid" %}
    </div>
</div>
<div class="caption">
    Confounders sit above both boxes and feed into each one, creating a fake link the regression mistakes for cause and effect.
</div>

---

### Getting closer: propensity-score matching

I can't randomly assign students to "study more," so I do the next best thing: pair up students with similar backgrounds (age, sleep, gender, marital status), so the main thing left separating the groups is how much they study. The love plot checks whether the groups actually became comparable.

<div class="row justify-content-center mt-3">
    <div class="col-sm-9">
        {% include figure.liquid loading="eager" path="assets/img/causal_love_plot.png" title="Covariate balance before and after matching" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    Red = before matching, teal = after. Everything inside the dashed ±0.1 band is well balanced. Matching pulls most covariates into the band, but sleep hours stays outside it, so that one is still not fully balanced.
</div>

<div class="row justify-content-center mt-3">
    <div class="col-sm-11">
        {% include figure.liquid loading="eager" path="assets/img/causal_psm_distributions.png" title="Propensity score distributions before and after matching" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    Before matching, the control group (bottom left) clusters at low propensity scores while the treated group sits high. After matching, the control distribution (bottom right) is reshaped to mirror the treated group, so the two are finally being compared on equal footing.
</div>

---

### The honest takeaway

There's no tidy "study X hours, gain Y GPA" number here, and that's the point. Matching fixed most of the imbalance but not all of it, and the data comes from a single college, so it can't fully settle the question. Knowing that, and knowing a raw correlation can point the wrong way, is the real skill. It's the same read you need for an A/B test that didn't randomize cleanly, which is most of the experiments that reach an analyst's desk.

---

**Stack:** R — Box-Cox OLS, propensity-score matching (full matching), love-plot balance diagnostics, with causal framing around omitted-variable bias and instrumental variables.

<a href="https://www.kaggle.com/datasets/nabilajahan/student-study-performance/data" class="btn btn-sm z-depth-0 mt-2" role="button">Dataset (Kaggle)</a>
