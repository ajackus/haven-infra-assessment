PS C:\Users\ghadg\Desktop\haven-infra-assessment\terraform> terraform init                           
Initializing the backend...                                                                          

Initializing provider plugins...
- Finding hashicorp/aws versions matching "~> 5.0"...
- Installing hashicorp/aws v5.100.0...
- Installed hashicorp/aws v5.100.0 (signed by HashiCorp)

Terraform has created a lock file .terraform.lock.hcl to record the provider
selections it made above. Include this file in your version control repository
so that Terraform can guarantee to make the same selections by default when
you run "terraform init" in the future.

Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see
any changes that are required for your infrastructure. All Terraform commands
should now work.

If you ever set or change modules or backend configuration for Terraform,
rerun this command to reinitialize your working directory. If you forget, other
commands will detect it and remind you to do so if necessary.
PS C:\Users\ghadg\Desktop\haven-infra-assessment\terraform> 
PS C:\Users\ghadg\Desktop\haven-infra-assessment\terraform> 
PS C:\Users\ghadg\Desktop\haven-infra-assessment\terraform> terraform plan
aws_s3_bucket.landlord_media[1]: Refreshing state... [id=haven-media-la-002]
aws_s3_bucket.landlord_media[2]: Refreshing state... [id=haven-media-la-003]
aws_s3_bucket.landlord_media[3]: Refreshing state... [id=haven-media-la-004]
aws_s3_bucket.landlord_media[0]: Refreshing state... [id=haven-media-la-001]

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with
the following symbols:
  + create

Terraform will perform the following actions:

  # aws_s3_bucket.landlord_media[0] will be created
  + resource "aws_s3_bucket" "landlord_media" {
      + acceleration_status         = (known after apply)
      + acl                         = (known after apply)
      + arn                         = (known after apply)
      + bucket                      = "haven-media-la-001"
      + bucket_domain_name          = (known after apply)
      + bucket_prefix               = (known after apply)
      + bucket_regional_domain_name = (known after apply)
      + force_destroy               = false
      + hosted_zone_id              = (known after apply)
      + id                          = (known after apply)
      + object_lock_enabled         = (known after apply)
      + policy                      = (known after apply)
      + region                      = (known after apply)
      + request_payer               = (known after apply)
      + tags                        = {
          + "landlord_account_id" = "la-001"
        }
      + tags_all                    = {
          + "landlord_account_id" = "la-001"
        }
      + website_domain              = (known after apply)
      + website_endpoint            = (known after apply)

      + cors_rule (known after apply)

      + grant (known after apply)

      + lifecycle_rule (known after apply)

      + logging (known after apply)

      + object_lock_configuration (known after apply)

      + replication_configuration (known after apply)

      + server_side_encryption_configuration (known after apply)

      + versioning (known after apply)

      + website (known after apply)
    }

  # aws_s3_bucket.landlord_media[1] will be created
  + resource "aws_s3_bucket" "landlord_media" {
      + acceleration_status         = (known after apply)
      + acl                         = (known after apply)
      + arn                         = (known after apply)
      + bucket                      = "haven-media-la-002"
      + bucket_domain_name          = (known after apply)
      + bucket_prefix               = (known after apply)
      + bucket_regional_domain_name = (known after apply)
      + force_destroy               = false
      + hosted_zone_id              = (known after apply)
      + id                          = (known after apply)
      + object_lock_enabled         = (known after apply)
      + policy                      = (known after apply)
      + region                      = (known after apply)
      + request_payer               = (known after apply)
      + tags                        = {
          + "landlord_account_id" = "la-002"
        }
      + tags_all                    = {
          + "landlord_account_id" = "la-002"
        }
      + website_domain              = (known after apply)
      + website_endpoint            = (known after apply)

      + cors_rule (known after apply)

      + grant (known after apply)

      + lifecycle_rule (known after apply)

      + logging (known after apply)

      + object_lock_configuration (known after apply)

      + replication_configuration (known after apply)

      + server_side_encryption_configuration (known after apply)

      + versioning (known after apply)

      + website (known after apply)
    }

  # aws_s3_bucket.landlord_media[2] will be created
  + resource "aws_s3_bucket" "landlord_media" {
      + acceleration_status         = (known after apply)
      + acl                         = (known after apply)
      + arn                         = (known after apply)
      + bucket                      = "haven-media-la-003"
      + bucket_domain_name          = (known after apply)
      + bucket_prefix               = (known after apply)
      + bucket_regional_domain_name = (known after apply)
      + force_destroy               = false
      + hosted_zone_id              = (known after apply)
      + id                          = (known after apply)
      + object_lock_enabled         = (known after apply)
      + policy                      = (known after apply)
      + region                      = (known after apply)
      + request_payer               = (known after apply)
      + tags                        = {
          + "landlord_account_id" = "la-003"
        }
      + tags_all                    = {
          + "landlord_account_id" = "la-003"
        }
      + website_domain              = (known after apply)
      + website_endpoint            = (known after apply)

      + cors_rule (known after apply)

      + grant (known after apply)

      + lifecycle_rule (known after apply)

      + logging (known after apply)

      + object_lock_configuration (known after apply)

      + replication_configuration (known after apply)

      + server_side_encryption_configuration (known after apply)

      + versioning (known after apply)

      + website (known after apply)
    }

  # aws_s3_bucket.landlord_media[3] will be created
  + resource "aws_s3_bucket" "landlord_media" {
      + acceleration_status         = (known after apply)
      + acl                         = (known after apply)
      + arn                         = (known after apply)
      + bucket                      = "haven-media-la-004"
      + bucket_domain_name          = (known after apply)
      + bucket_prefix               = (known after apply)
      + bucket_regional_domain_name = (known after apply)
      + force_destroy               = false
      + hosted_zone_id              = (known after apply)
      + id                          = (known after apply)
      + object_lock_enabled         = (known after apply)
      + policy                      = (known after apply)
      + region                      = (known after apply)
      + request_payer               = (known after apply)
      + tags                        = {
          + "landlord_account_id" = "la-004"
        }
      + tags_all                    = {
          + "landlord_account_id" = "la-004"
        }
      + website_domain              = (known after apply)
      + website_endpoint            = (known after apply)

      + cors_rule (known after apply)

      + grant (known after apply)

      + lifecycle_rule (known after apply)

      + logging (known after apply)

      + object_lock_configuration (known after apply)

      + replication_configuration (known after apply)

      + server_side_encryption_configuration (known after apply)

      + versioning (known after apply)

      + website (known after apply)
    }

  # aws_s3_bucket.listing_media will be created
  + resource "aws_s3_bucket" "listing_media" {
      + acceleration_status         = (known after apply)
      + acl                         = (known after apply)
      + arn                         = (known after apply)
      + bucket                      = "haven-listing-media"
      + bucket_domain_name          = (known after apply)
      + bucket_prefix               = (known after apply)
      + bucket_regional_domain_name = (known after apply)
      + force_destroy               = false
      + hosted_zone_id              = (known after apply)
      + id                          = (known after apply)
      + object_lock_enabled         = (known after apply)
      + policy                      = (known after apply)
      + region                      = (known after apply)
      + request_payer               = (known after apply)
      + tags_all                    = (known after apply)
      + website_domain              = (known after apply)
      + website_endpoint            = (known after apply)

      + cors_rule (known after apply)

      + grant (known after apply)

      + lifecycle_rule (known after apply)

      + logging (known after apply)

      + object_lock_configuration (known after apply)

      + replication_configuration (known after apply)

      + server_side_encryption_configuration (known after apply)

      + versioning (known after apply)

      + website (known after apply)
    }

  # aws_s3_bucket_lifecycle_configuration.listing_media_archive will be created
  + resource "aws_s3_bucket_lifecycle_configuration" "listing_media_archive" {
      + bucket                                 = (known after apply)
      + expected_bucket_owner                  = (known after apply)
      + id                                     = (known after apply)
      + transition_default_minimum_object_size = "all_storage_classes_128K"

      + rule {
          + id     = "archive-sold-listing-photos"
          + status = "Enabled"
            # (1 unchanged attribute hidden)

          + transition {
              + days          = 30
              + storage_class = "GLACIER"
            }
        }
    }

Plan: 6 to add, 0 to change, 0 to destroy.
╷
│ Warning: Invalid Attribute Combination
│ 
│   with aws_s3_bucket_lifecycle_configuration.listing_media_archive,
│   on lifecycle.tf line 18, in resource "aws_s3_bucket_lifecycle_configuration" "listing_media_archive":
│   18:   rule {
│ 
│ No attribute specified when one (and only one) of [rule[0].filter,rule[0].prefix] is required
│ 
│ This will be an error in a future version of the provider
╵

─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

Note: You didn't use the -out option to save this plan, so Terraform can't guarantee to take exactly these actions if
you run "terraform apply" now.
PS C:\Users\ghadg\Desktop\haven-infra-assessment\terraform> 



#####pytest

PS C:\Users\ghadg\Desktop\haven-infra-assessment> pytest -v                   
================================================ test session starts ================================================
platform win32 -- Python 3.12.10, pytest-9.2.0, pluggy-1.7.0 -- C:\Users\ghadg\AppData\Local\Programs\Python\Python312\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\ghadg\Desktop\haven-infra-assessment
collected 0 items                                                                                                    

=============================================== no tests ran in 0.19s ===============================================
PS C:\Users\ghadg\Desktop\haven-infra-assessment> 


## B2 Test & Idempotency Runs.
platform win32 -- Python 3.12.10, pytest-9.2.0, pluggy-1.7.0 -- C:\Users\ghadg\AppData\Local\Programs\Python\Python312\python.exe

tests/test_access_control.py::test_allows_same_account_access PASSED                                           [ 20%]
tests/test_access_control.py::test_denies_cross_account_access PASSED                                          [ 40%]
tests/test_cost_tag_check.py::test_reports_resources_missing_landlord_account_tag PASSED                       [ 60%]
tests/test_cost_tag_check.py::test_is_idempotent PASSED                                                        [ 80%]
tests/test_cost_tag_check.py::test_checks_tags_all_without_resource_type_specific_logic PASSED                 [100%]

================================================= 5 passed in 0.19s =================================================
PS C:\Users\ghadg\Desktop\haven-infra-assessment> ^C
PS C:\Users\ghadg\Desktop\haven-infra-assessment> 
PS C:\Users\ghadg\Desktop\haven-infra-assessment> 
PS C:\Users\ghadg\Desktop\haven-infra-assessment> python scripts/cost_tag_check.py fixtures/plan.json
Missing landlord_account_id tag: aws_lambda_function.mls_feed_sync
Missing landlord_account_id tag: aws_s3_bucket.listing_media
PS C:\Users\ghadg\Desktop\haven-infra-assessment> 
PS C:\Users\ghadg\Desktop\haven-infra-assessment> 
PS C:\Users\ghadg\Desktop\haven-infra-assessment> python scripts/cost_tag_check.py fixtures/plan.json
Missing landlord_account_id tag: aws_lambda_function.mls_feed_sync
Missing landlord_account_id tag: aws_s3_bucket.listing_media
PS C:\Users\ghadg\Desktop\haven-infra-assessment> 
