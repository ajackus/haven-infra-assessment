from cost_tag_check import validate_tags


def test_missing_landlord_tag():
    plan = {
        "planned_values": {
            "root_module": {
                "resources": [
                    {
                        "address": "aws_s3_bucket.test",
                        "values": {
                            "tags": {
                                "tenant_id": "T001"
                            }
                        }
                    }
                ]
            }
        }
    }

    assert validate_tags(plan) == [
        "aws_s3_bucket.test"
    ]


def test_valid_landlord_tag():
    plan = {
        "planned_values": {
            "root_module": {
                "resources": [
                    {
                        "address": "aws_s3_bucket.test",
                        "values": {
                            "tags": {
                                "tenant_id": "T001",
                                "landlord_account_id": "L001"
                            }
                        }
                    }
                ]
            }
        }
    }

    assert validate_tags(plan) == []


def test_idempotency():
    plan = {
        "planned_values": {
            "root_module": {
                "resources": [
                    {
                        "address": "aws_s3_bucket.test",
                        "values": {
                            "tags": {
                                "tenant_id": "T001"
                            }
                        }
                    }
                ]
            }
        }
    }

    first_result = validate_tags(plan)
    second_result = validate_tags(plan)

    assert first_result == second_result



