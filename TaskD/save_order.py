import boto3
import uuid
from decimal import Decimal
from datetime import datetime, timezone

dynamodb = boto3.resource("dynamodb")
orders_table = dynamodb.Table("SanChaOrders")


def lambda_handler(event, context):

    try:
        # Accept output directly from ValidateOrder
        order = event.get("order", event)

        if not order:
            raise ValueError(
                "Order information is missing."
            )

        order_id = str(uuid.uuid4())

        saved_order = {
            "orderId": order_id,
            "customerName":
                order["customerName"],
            "customerEmail":
                order["customerEmail"],
            "items":
                order["items"],
            "totalAmount":
                Decimal(
                    str(order["totalAmount"])
                ),
            "status":
                "RECEIVED",
            "createdAt":
                datetime.now(
                    timezone.utc
                ).isoformat()
        }

        # Convert prices back to DynamoDB Numbers
        for item in saved_order["items"]:
            item["unitPrice"] = Decimal(
                str(item["unitPrice"])
            )

            item["lineTotal"] = Decimal(
                str(item["lineTotal"])
            )

        orders_table.put_item(
            Item=saved_order
        )

        return {
            "success": True,
            "orderId": order_id,
            "status": "RECEIVED"
        }

    except Exception as error:

        return {
            "success": False,
            "error": str(error)
        }