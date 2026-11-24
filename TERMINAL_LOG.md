# Terminal Log

## Verification status

The implementation and tests are committed, but this file must be completed with
actual output from a run in the assessment repository. No Terraform plan or
repository pytest output is claimed until those commands are run locally.

## Environment and setup

Paste the actual output for:

```text
git clone https://github.com/rajaty/haven-infra-assessment.git
cd haven-infra-assessment
terraform version
python --version
python -m venv .venv
# Activate the virtual environment for your shell.
pip install -r requirements.txt
```

## B0 reproduction

Temporarily remove `la-002` from the default landlord list, then run
`terraform plan -refresh=false` from `terraform/`. Paste the actual relevant
resource actions and plan summary. Restore the input list afterwards.

## B2 tests

Run `python -m pytest -q` and paste the actual output.

## Cost-tag check — first run

Run `python scripts/cost_tag_check.py fixtures/plan.json`. Paste the complete
output and exit code.

## Cost-tag check — second run, unchanged plan

Run the same command again without changing the plan. Paste the complete
output and exit code. Verify the output and exit code match the first run.

The fixture's expected policy result is non-zero because
`aws_s3_bucket.listing_media` and `aws_lambda_function.mls_feed_sync` lack
`landlord_account_id`. This expected policy failure is distinct from pytest
test success.
