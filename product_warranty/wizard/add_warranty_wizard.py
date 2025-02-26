from odoo import api, Command, fields, models


class AddWarrantyWizard(models.TransientModel):
    _name = 'add.warranty.wizard'
    _description = 'Add Warranty Wizard'

    sale_order = fields.Many2one(comodel_name='sale.order', string="Order", required=True)
    warranty_lines = fields.One2many(
        comodel_name='warranty.wizard.line', inverse_name='wizard_id', string="Warranty lines"
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        sale_order = self.env["sale.order"].browse(self.env.context.get("active_id"))
        res.update({
            'sale_order': sale_order.id,
            'warranty_lines': [
                Command.create(
                    {
                        "sale_order_line": line.id,
                        "warranty_config": False,
                    } for line in sale_order.order_line.filtered(lambda line: 
                        line.product_template_id and line.product_template_id.is_warranty
                    )
                )
            ]
        })
        return res
   
    def apply_warranty(self):
        extended_warranty_product = self.env.ref("product_warranty.extended_warranty_product_tmpl").id
        warranty_line_vals = [
            {
                "order_id": self.sale_order.id,
                "product_id": extended_warranty_product,
                "product_uom_qty": line.sale_order_line.product_uom_qty,
                "linked_line_id": line.sale_order_line.id,
                "price_unit": (line.warranty_config.percentage / 100) * line.sale_order_line.price_unit,
            }
            for line in self.warranty_lines if line.warranty_config
        ]
        if warranty_line_vals:
            self.env["sale.order.line"].create(warranty_line_vals)
