import boto3

dynamodb = boto3.client("dynamodb")

PRODUCT_TABLE = "SanChaProducts"
ORDER_TABLE = "SanChaOrders"


def create_products_table():
    try:
        dynamodb.create_table(
            TableName=PRODUCT_TABLE,

            KeySchema=[
                {
                    "AttributeName": "productId",
                    "KeyType": "HASH"
                }
            ],

            AttributeDefinitions=[
                {
                    "AttributeName": "productId",
                    "AttributeType": "S"
                },
                {
                    "AttributeName": "category",
                    "AttributeType": "S"
                },
                {
                    "AttributeName": "price",
                    "AttributeType": "N"
                }
            ],

            GlobalSecondaryIndexes=[
                {
                    "IndexName": "CategoryPriceIndex",

                    "KeySchema": [
                        {
                            "AttributeName": "category",
                            "KeyType": "HASH"
                        },
                        {
                            "AttributeName": "price",
                            "KeyType": "RANGE"
                        }
                    ],

                    "Projection": {
                        "ProjectionType": "ALL"
                    }
                }
            ],

            BillingMode="PAY_PER_REQUEST"
        )

        print("Creating SanChaProducts...")

        waiter = dynamodb.get_waiter("table_exists")

        waiter.wait(
            TableName=PRODUCT_TABLE
        )

        print("SanChaProducts created successfully.")

    except dynamodb.exceptions.ResourceInUseException:
        print("SanChaProducts already exists.")


def create_orders_table():
    try:
        dynamodb.create_table(
            TableName=ORDER_TABLE,

            KeySchema=[
                {
                    "AttributeName": "orderId",
                    "KeyType": "HASH"
                }
            ],

            AttributeDefinitions=[
                {
                    "AttributeName": "orderId",
                    "AttributeType": "S"
                }
            ],

            BillingMode="PAY_PER_REQUEST"
        )

        print("Creating SanChaOrders...")

        waiter = dynamodb.get_waiter("table_exists")

        waiter.wait(
            TableName=ORDER_TABLE
        )

        print("SanChaOrders created successfully.")

    except dynamodb.exceptions.ResourceInUseException:
        print("SanChaOrders already exists.")


create_products_table()
create_orders_table()