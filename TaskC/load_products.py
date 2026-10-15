import boto3
import csv
from decimal import Decimal

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("SanChaProducts")

with open("products.csv", newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)

    with table.batch_writer() as batch:
        for row in reader:
            item = {
                "productId": row["product_id"],
                "name": row["name"],
                "category": row["category"],
                "description": row["description"],
                "price": Decimal(row["price"]),
                "image": row["image"]
            }

            batch.put_item(Item=item)

            print(
                f"Added {row['product_id']} - {row['name']}"
            )

print("All products uploaded successfully.")