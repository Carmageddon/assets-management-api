import pytest
from app.owners.utils import evaluate_condition

def test_simple_condition():
    asset = {"type": "ec2-instance"}
    condition = {"type": "ec2-instance"}
    assert evaluate_condition(asset, condition) == True

def test_simple_condition_false():
    asset = {"type": "ec2-instance"}
    condition = {"type": "s3-bucket"}
    assert evaluate_condition(asset, condition) == False

def test_and_condition():
    asset = {"type": "ec2-instance", "name": "prod-instance"}
    condition = {"AND": [{"type": "ec2-instance"}, {"name_contains": "prod"}]}
    assert evaluate_condition(asset, condition) == True

def test_and_condition_false():
    asset = {"type": "ec2-instance", "name": "test-instance"}
    condition = {"AND": [{"type": "ec2-instance"}, {"name_contains": "prod"}]}
    assert evaluate_condition(asset, condition) == False

def test_or_condition():
    asset = {"type": "ec2-instance", "name": "test-instance"}
    condition = {"OR": [{"type": "s3-bucket"}, {"name_contains": "test"}]}
    assert evaluate_condition(asset, condition) == True

def test_or_condition_false():
    asset = {"type": "ec2-instance", "name": "prod-instance"}
    condition = {"OR": [{"type": "s3-bucket"}, {"name_contains": "test"}]}
    assert evaluate_condition(asset, condition) == False

def test_nested_attributes():
    asset = {"tags": [{"key": "env", "value": "prod"}]}
    condition = {"tags": [{"key": "env", "value": "prod"}]}
    assert evaluate_condition(asset, condition) == True

def test_nested_attributes_false():
    asset = {"tags": [{"key": "env", "value": "dev"}]}
    condition = {"tags": [{"key": "env", "value": "prod"}]}
    assert evaluate_condition(asset, condition) == False

def test_name_contains():
    asset = {"name": "production-instance"}
    condition = {"name_contains": "prod"}
    assert evaluate_condition(asset, condition) == True

def test_name_contains_false():
    asset = {"name": "test-instance"}
    condition = {"name_contains": "prod"}
    assert evaluate_condition(asset, condition) == False

def test_complex_rule_with_and_or_conditions_false():
    asset = {
        "_id": {"$oid": "66abe3b1fb3f5484368dfe66"},
        "id": "16",
        "name": "Test Asset 16",
        "type": "s3-bucket",
        "tags": [{"key": "env", "value": "prod"}],
        "cloud_account": {"id": "acc6", "name": "Test Account 6"},
        "owner_id": "1",
        "region": "us-west-1",
        "group_name": "S3 Resources"
    }
    
    condition = {
        "AND": [
            {"type": "ec2-instance"},
            {"OR": [{"tags": [{"key": "env", "value": "prod"}]}, {"name_contains": "prod"}]}
        ]
    }

    assert evaluate_condition(asset, condition) == False

def test_complex_rule_with_and_or_conditions_true():
    asset = {
        "id": "16",
        "name": "prod-asset-16",
        "type": "ec2-instance",
        "tags": [{"key": "env", "value": "prod"}],
        "cloud_account": {"id": "acc6", "name": "Test Account 6"},
        "owner_id": "1",
        "region": "us-west-1",
        "group_name": "EC2 Resources"
    }
    
    condition = {
        "AND": [
            {"type": "ec2-instance"},
            {"OR": [{"tags": [{"key": "env", "value": "prod"}]}, {"name_contains": "prod"}]}
        ]
    }
    
    assert evaluate_condition(asset, condition) == True

def test_new_attribute_contains():
    asset = {
        "id": "17",
        "name": "Test Asset 17",
        "alias": "prod-alias-17",
        "type": "s3-bucket",
        "tags": [{"key": "env", "value": "test"}],
        "cloud_account": {"id": "acc7", "name": "Test Account 7"},
        "owner_id": "2",
        "region": "us-east-1",
        "group_name": "S3 Resources"
    }
    
    condition = {"alias_contains": "prod"}
    
    assert evaluate_condition(asset, condition) == True

def test_combined_conditions():
    asset = {
        "id": "18",
        "name": "dev-asset-18",
        "type": "rds-instance",
        "tags": [{"key": "env", "value": "dev"}],
        "cloud_account": {"id": "acc8", "name": "Test Account 8"},
        "owner_id": "3",
        "region": "eu-central-1",
        "group_name": "RDS Resources"
    }
    
    condition = {
        "AND": [
            {"type": "rds-instance"},
            {"OR": [{"tags": [{"key": "env", "value": "prod"}]}, {"name_contains": "dev"}]}
        ]
    }
    
    assert evaluate_condition(asset, condition) == True

if __name__ == "__main__":
    pytest.main()
