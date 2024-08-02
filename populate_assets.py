from os import name
import random
import logging
from app import create_app, mongo

logging.basicConfig(level=logging.INFO)

def generate_asset(id):
    return {
        "id": str(id),
        "name": f"Test Asset {id}",
        "type": random.choice(["ec2-instance", "s3-bucket", "rds-instance"]),
        "tags": [{"key": "env", "value": random.choice(["prod", "dev", "test"])}],
        "cloud_account": {"id": f"acc{id % 10}", "name": f"Test Account {id % 10}"},
        "owner_id": f"owner{id % 5}",
        "region": random.choice(["us-west-1", "us-east-1", "eu-central-1"]),
        "group_name": None
    }

def populate_database(n):
    app = create_app()
    with app.app_context():
        for i in range(n):
            mongo.db.assets.insert_one(generate_asset(i))
            if i % 100 == 0:
                logging.info(f"Inserted {i} assets")
        logging.info(f"Inserted {n} assets into the database")
        print(f"Inserted {n} assets into the database")

if __name__ == "__main__":
    populate_database(1000)