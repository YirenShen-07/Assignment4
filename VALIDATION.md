# Verification

Verified on 2026-10-13 (UTC) with Python 3.12 and the pinned requirements.

- The analysis CLI completed and generated the committed reports.
- All 6 notebook code cells executed without errors using in-process IPython; notebook format was validated. The standard Jupyter kernel transport was unavailable in this verification environment, so this is not a claim of a separate-kernel test.
- README links to local assets and results were checked.
- The original-source audit matched all 303 bundled rows and confirmed inverted target coding. Three-fold training-only CV and the 91-row held-out evaluation were rerun after missing-code correction.
