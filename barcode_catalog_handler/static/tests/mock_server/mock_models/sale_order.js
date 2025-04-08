import { fields, models } from "@web/../tests/web_test_helpers";

export class SaleOrder extends models.Model {
    _name = "sale.order";

    order_line = fields.One2many({ relation: "sale.order.line", string: "Sale Order Lines" });

    _records = [
        {
            id: 1,
            order_line: [1]
        },
    ];
}
