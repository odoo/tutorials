import { fields, models } from "@web/../tests/web_test_helpers";

export class PurchaseOrderLine extends models.Model {
    _name = "purchase.order.line";

    id = fields.Integer();
    order_id = fields.Many2one({ relation: "purchase.order", string: "Purchase Order" });
    product_id = fields.Many2one({ relation: "product.product", string: "Product" });
    product_qty = fields.Float({ string: "Quantity" });

    _records = [
        {
            id: 1,
            order_id: 1,
            product_id: 2,
            product_qty: 2
        },
    ];
}
