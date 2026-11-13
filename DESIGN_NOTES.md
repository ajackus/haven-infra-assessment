# Design Notes

## B2 — idempotency key

State exactly what key your `cost_tag_check.py` uses to decide whether two resources in the
same run are "the same" for dedup purposes, and why running it twice against an unchanged
plan file produces identical output and exit code without the script keeping any record
between runs. Use the word "idempotency" in your explanation.

<!-- To guarantee idempotency , cost_tag_check.py deduplicates resources within a run using the terraform resources 'address' (eg, aws_s3_bucket.listing_media, or the composite keyt (resource[]""address")) as the unique key and sort all flagged voilations by address. -->

## Any other decision with a non-obvious alternative

<!--  beacuse cost_tag_check.py operqaates as a pure, stateless function over the input terraform plan JSON- woothout writing external state files, mutating input data, or injecting timestamos or random identifies runningit twice againtst an unchanged plan file evaluates the exact same resources adresses and produce byte-for -byte identical outpiut and exit codes. -->
