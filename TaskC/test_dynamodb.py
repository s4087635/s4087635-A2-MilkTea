import boto3
from boto3.dynamodb.conditions import Key
from decimal import Decimal

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("SanChaProducts")


# TEST 1 - Retrieve a product using the primary key
print("\n--- TEST 1: PRIMARY KEY RETRIEVAL ---")

response = table.get_item(
    Key={
        "productId": "P001"
    }
)

product = response.get("Item")

if product:
    print(
        product["productId"],
        product["name"],
        product["category"],
        "$" + str(product["price"])
    )
else:
    print("Product not found")


# TEST 2 - Query products using the GSI by category
print("\n--- TEST 2: GSI CATEGORY QUERY ---")

response = table.query(
    IndexName="CategoryPriceIndex",
    KeyConditionExpression=Key("category").eq("Milk Tea")
)

for item in response["Items"]:
    print(
        item["productId"],
        item["name"],
        item["category"],
        "$" + str(item["price"])
    )


# TEST 3 - Query Milk Tea products within a price range
print("\n--- TEST 3: CATEGORY AND PRICE RANGE QUERY ---")

response = table.query(
    IndexName="CategoryPriceIndex",
    KeyConditionExpression=
        Key("category").eq("Milk Tea")
        &
        Key("price").between(
            Decimal("6.50"),
            Decimal("7.00")
        )
)

for item in response["Items"]:
    print(
        item["productId"],
        item["name"],
        "$" + str(item["price"])
    )