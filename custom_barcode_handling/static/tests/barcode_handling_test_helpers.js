import { mailModels } from "@mail/../tests/mail_test_helpers";
import { defineModels, models, fields } from "@web/../tests/web_test_helpers";

export function defineBarcodeHandlingModels() {
    return defineModels({ Product, SaleOrderLine, SaleOrder, PurchaseOrder, PurchaseOrderLine, ...mailModels });
}

class Product extends models.Model {
    _name = "product.product";
    name = fields.Char();
    barcode = fields.Char();

    _records = [
        { id: 1, name: "iPhone", barcode: "123456789" },
        { id: 2, name: "iPad", barcode: "987654321" },
    ];

    _views = {
        kanban: 
        `<kanban js_class='product_kanban_catalog'>
            <templates>
                <t t-name="card">
                    <field name="id"/>
                    <field name="name"/>
                    <div name="o_kanban_price"
                        t-attf-id="product-{{record.id.raw_value}}-price"
                        class="d-flex flex-column"/>
                </t>
            </templates>
        </kanban>`,
    }
}

class SaleOrder extends models.Model {
    _name = "sale.order";

    order_line = fields.One2many({ relation: "sale.order.line" });

    _records = [
        { id: 1, order_line: [1] },
        { id: 2, order_line: [2] },
    ];
}

class SaleOrderLine extends models.Model {
    _name = "sale.order.line";

    id = fields.Integer();
    name = fields.Text();
    product_id = fields.Many2one({ relation: "product.product" });
    product_uom_qty = fields.Float();
    quantity = fields.Float();
    order_id = fields.Many2one({ relation: "sale.order" });

    _records = [
        { id: 1, name: "iPad", product_id: 2, product_uom_qty: 1, order_id: 1 },
        { id: 2, name: "iPhone", product_id: 1, product_uom_qty: 1, order_id: 2 },
    ];
}


class PurchaseOrder extends models.Model {
    _name = "purchase.order";

    order_line = fields.One2many({ relation: "purchase.order.line" });

    _records = [
        { id: 1, order_line: [1] },
        { id: 2, order_line: [2] },
    ];
}

class PurchaseOrderLine extends models.Model {
    _name = "purchase.order.line";

    id = fields.Integer();
    name = fields.Text();
    product_id = fields.Many2one({ relation: "product.product" });
    product_qty = fields.Float();
    quantity = fields.Float();
    order_id = fields.Many2one({ relation: "purchase.order" });

    _records = [
        { id: 1, name: "iPad", product_id: 2, product_qty: 1, order_id: 1 },
        { id: 2, name: "iPhone", product_id: 1, product_qty: 1, order_id: 2 },
    ];
}