import { fields, models } from "@web/../tests/web_test_helpers";

export class PurchaseOrder extends models.Model {
    _name = "purchase.order";

    order_line = fields.One2many({ relation: "purchase.order.line", string: "Purchase Order Lines" });

    _records = [
        {
            id: 1,
            order_line: [1]
        },
    ];
}
