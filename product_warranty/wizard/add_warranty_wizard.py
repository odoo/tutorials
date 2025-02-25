from odoo import Command, models, fields, api


class AddWarrantyWizard(models.TransientModel):
    _name = 'add.warranty.wizard'
    _description = 'Add Warranty Wizard'

    sale_order = fields.Many2one(comodel_name='sale.order', string='Order', required=True)
    warranty_lines = fields.One2many(
        comodel_name='warranty.wizard.line', inverse_name='wizard_id', string=' Warranty lines'
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        sale_order = self.env["sale.order"].browse(self.env.context.get("active_id"))
        warranty_lines = []
        for line in sale_order.order_line.filtered(
            lambda line: line.product_template_id
            and line.product_template_id.is_warranty
        ):
            warranty_lines.append(
                Command.create(
                    {
                        "sale_order_line": line.id,
                        "warranty_config": False,
                    }
                )
            )
        res["sale_order"] = sale_order.id
        res["warranty_lines"] = warranty_lines
        return res 
   
    def apply_warranty(self):
        for line in self.warranty_lines:
            product = self.env["product.template"].browse(line.product_template.id)
            if line.warranty_config:
                self.env["sale.order.line"].create(
                    {
                        "order_id": self.sale_order.id,
                        "name": "Extended Warranty of %d Years - %s"
                        % (line.warranty_config.years, product.name),
                        "product_template_id": line.product_template.id,
                        "product_uom_qty": line.sale_order_line.product_uom_qty,
                        "linked_line_id": line.sale_order_line.id,
                        "price_unit": (line.warranty_config.percentage / 100) * line.sale_order_line.price_unit,
                    }
                )
