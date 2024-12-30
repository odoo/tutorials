from odoo import models, fields, api


class AddWarrantyWizard(models.TransientModel):
    _name = "add.warranty.wizard"
    _description = "Add Warranty Wizard"

    product_ids = fields.One2many(
        "add.warranty.line.wizard", "warranty_line_id", string="Products"
    )
    
    def apply_warranty(self):
        for record in self.product_ids:
            if record.year:
                self.env["sale.order.line"].create(
                    {
                        "sequence": record.main_order_line.sequence + 1,
                        "product_id": record.year.product_id.id,
                        "product_uom_qty": record.main_order_line.product_uom_qty,
                        "order_id": self._context.get("active_id"),
                        "price_unit": record.product_id.list_price
                        * record.year.percentage
                        / 100,
                        "warranty_line_id": record.main_order_line.id,
                        "name": "For "
                        + record.main_order_line.name
                        + ", End Date: "
                        + str(record.end_date),
                    }
                )
