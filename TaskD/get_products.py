import boto3
import json
from boto3.dynamodb.conditions import Key
from decimal import Decimal

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("SanChaProducts")


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)


def lambda_handler(event, context):
    try:
        category = None

        # Allows direct Lambda testing
        if event.get("category"):
            category = event["category"]

        # Allows API Gateway use later
        query_params = event.get("queryStringParameters")

        if query_params:
            category = query_params.get("category")

        if category:
            response = table.query(
                IndexName="CategoryPriceIndex",
                KeyConditionExpression=
                    Key("category").eq(category)
            )
        else:
            response = table.scan()

        products = response.get("Items", [])

        return {
            "statusCode": 200,
            "body": json.dumps(
                products,
                cls=DecimalEncoder
            )
        }

    except Exception as error:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": str(error)
            })
        }