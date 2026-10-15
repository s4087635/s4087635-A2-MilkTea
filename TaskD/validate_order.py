import boto3
import re
from decimal import Decimal

dynamodb = boto3.resource("dynamodb")
products_table = dynamodb.Table("SanChaProducts")


def lambda_handler(event, context):

    errors = []

    customer_name = event.get("customerName", "").strip()
    customer_email = event.get("customerEmail", "").strip()
    items = event.get("items", [])

    # Validate customer name
    if not customer_name:
        errors.append("Customer name is required.")
    elif len(customer_name) < 2:
        errors.append("Customer name is too short.")

    # Validate email
    email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    if not customer_email:
        errors.append("Customer email is required.")
    elif not re.match(email_pattern, customer_email):
        errors.append("Customer email is invalid.")

    # Validate items
    if not isinstance(items, list) or len(items) == 0:
        errors.append(
            "At least one product must be ordered."
        )

    validated_items = []
    total_amount = Decimal("0.00")

    for item in items:

        product_id = item.get("productId")
        quantity = item.get("quantity")

        if not product_id:
            errors.append("Product ID is required.")
            continue

        try:
            quantity = int(quantity)

            if quantity < 1:
                raise ValueError()

        except (ValueError, TypeError):
            errors.append(
                f"Invalid quantity for {product_id}."
            )
            continue

        response = products_table.get_item(
            Key={
                "productId": product_id
            }
        )

        product = response.get("Item")

        if not product:
            errors.append(
                f"Product {product_id} does not exist."
            )
            continue

        unit_price = product["price"]
        line_total = unit_price * quantity

        total_amount += line_total

        validated_items.append({
            "productId": product_id,
            "productName": product["name"],
            "quantity": quantity,
            "unitPrice": str(unit_price),
            "lineTotal": str(line_total)
        })

    if errors:
        return {
            "valid": False,
            "errors": errors
        }

    return {
        "valid": True,

        "order": {
            "customerName": customer_name,
            "customerEmail": customer_email,
            "items": validated_items,
            "totalAmount": str(total_amount)
        }
    }