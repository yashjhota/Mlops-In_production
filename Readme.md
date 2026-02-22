**First Stage: Structured Pipeline Design**

We split the ML lifecycle into separate modules:

• ingest.py → brings new raw data into the system

• preprocess.py → cleans and prepares data

• train.py → trains the model and logs experiment details

• evaluate.py → evaluates the model and decides if it’s good

• pipeline.py → orchestrates all steps

Why this matters:

In real systems, responsibilities must be separated.

One file = one job.

If something breaks, you know where to look.

This is basic software engineering applied to ML.

---

**Second Stage: Reproducibility & Logging (MLflow)**

We integrated MLflow to log:

• Parameters (hyperparameters, dataset hash)

• Metrics (accuracy, precision, recall, F1)

• Artifacts (model file, plots, tokenizer, etc.)

This gave us experiment tracking.

Why this matters:

Without experiment tracking, ML becomes guesswork.

With MLflow:

Every run is recorded.

Every model can be traced.

Every metric has context.

That’s scientific discipline.

---

Third Stage: Data Versioning via Hashing

We added dataset fingerprinting using MD5 hash.

Every training run logs the exact dataset hash.

Why this matters:

If a model performs well, you must know exactly which data produced it.

This prevents “it worked last week but I don’t know why” syndrome.

Reproducibility is the backbone of MLOps.

---

Fourth Stage: Model Promotion Logic

We implemented automatic comparison:

If new model’s metric > previous best → promote it

Else → reject it

The promoted model is saved as:

production_model.pkl

This introduces a decision system.

Why this matters:

Production ML is not about training.

It’s about selecting.

You built a simple model registry behavior.

That is very close to how real ML model lifecycle management works.

---

Fifth Stage: Serving Layer (FastAPI)

We created a prediction API:

• Loads production_model.pkl

• Exposes /predict endpoint

• Serves predictions via HTTP

This separates training from serving.

Why this matters:

Training systems should not interfere with live inference systems.

Separation of concerns is critical.

We also added automatic model reload if the production file changes.

That means:

Pipeline upgrades model

API starts using it automatically

That’s dynamic deployment behavior.

---

Sixth Stage: Prediction Logging

Every inference call:

• Logs timestamp

• Logs input

• Logs prediction

Saved to logs/predictions.jsonl

Why this matters:

Production systems must observe real-world usage.

Without logging predictions, you cannot detect degradation.

---

Seventh Stage: Basic Drift Detection

We saved training statistics (mean of training data).

In the API, we compare live input to training distribution.

If deviation is large → print drift alert.

Is it mathematically perfect? No.

Is it conceptually correct? Yes.

You introduced monitoring of production data against training assumptions.

That is real MLOps thinking.

---

Eighth Stage: Monitoring Script

We added monitor.py to:

• Read prediction logs

• Summarize behavior

• Provide basic operational visibility

Now your system isn’t blind.

---

Ninth Stage: Containerization with Docker

We:

• Created Dockerfile

• Built image

• Ran API inside container

• Ran pipeline inside container

• Added volume mapping for persistence

Why this matters:

Containers provide:

Isolation

Reproducibility

Environment consistency

Now your ML system is portable.

It can run anywhere Docker runs.

That’s infrastructure maturity.
