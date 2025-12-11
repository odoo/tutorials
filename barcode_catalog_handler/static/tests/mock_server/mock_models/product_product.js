import { fields, models } from "@web/../tests/web_test_helpers";

export class Product extends models.Model {
    _name = "product.product";

    name = fields.Char({ string: "Product Name" });
    barcode = fields.Char({ string: "Barcode" });

    _records = [
        {
            id: 1,
            name: "Table",
            barcode: "123456789"
        },
        {
            id: 2,
            name: "Chair",
            barcode: "987654321"
        },
    ];

    _views = {
        kanban:
                `<kanban js_class="product_kanban_catalog">
                    <templates>
                        <t t-name="card">
                            <h3 class="card-title fw-bold text-primary">
                                <field name="name"/>
                            </h3>
                            <strong class="text-success">
                                <div name="o_kanban_price"
                                    t-attf-id="product-{{record.id.raw_value}}-price"
                                    class="d-flex flex-column"/>
                            </strong>
                        </t>
                    </templates>
                </kanban>
            `,
    };
}
