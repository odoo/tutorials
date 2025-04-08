import { fields, models } from "@web/../tests/web_test_helpers";

export class SaleOrderLine extends models.Model {
    _name = "sale.order.line";

    id = fields.Integer();
    order_id = fields.Many2one({ relation: "sale.order", string: "Sale Order" });
    product_id = fields.Many2one({ relation: "product.product", string: "Product" });
    product_uom_qty = fields.Float({ string: "Quantity" });

    _records = [
        {
            id: 1,
            order_id: 1,
            product_id: 1,
            product_uom_qty: 1
        },
    ];
}
