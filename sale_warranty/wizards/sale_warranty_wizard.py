from odoo import api, fields, models
from odoo.exceptions import UserError


class SaleStockWarrantyWizard(models.TransientModel):
    _name = 'sale.warranty.wizard'
    _description = 'Wizard window to choose warranty for the product'

    warranty_line_ids = fields.One2many(comodel_name='sale.warranty.wizard.line', inverse_name='warranty_wizard_id', string='Warranty Lines')
    sale_order_id = fields.Many2one(comodel_name='sale.order', string='Source Order')

    @api.model
    def default_get(self, values):
        res = super().default_get(values)
        if self.env.context.get('active_id'):
            sale_order_id = self.env['sale.order'].browse(self.env.context['active_id'])
            sale_order_line_id = sale_order_id.order_line.filtered(lambda l: l.product_template_id.is_warranty_available)

            warranty_lines_data = [
                (
                    0,0,{
                        "product_id": line.product_id.id,
                        "quantity": line.product_uom_qty,
                        "sale_order_line_id": line.id
                    },
                )
                for line in sale_order_line_id
            ]

            res.update({
                'sale_order_id': sale_order_id.id,
                'warranty_line_ids': warranty_lines_data
            })

        return res

    def action_add_warranty(self):
        for line in self.warranty_line_ids:
            if not line.warranty_configuration_id:
                raise UserError("Warranty Configuration is required for all warranty lines.")

        warranty_lines = []

        for line in self.warranty_line_ids:

            warranty_lines.append({
                "order_id": self.sale_order_id.id,
                "product_id": line.warranty_configuration_id.product_id.id,
                "name": "End Date: " + fields.Date.to_string( line.end_date ),
                "product_uom_qty": line.quantity,
                "price_unit": line.product_id.list_price * (line.warranty_configuration_id.percentage / 100),
                "source_order_line_id": line.sale_order_line_id.id,
                "sequence": line.sale_order_line_id.sequence
            })

        if warranty_lines:
            self.env['sale.order.line'].create(warranty_lines)
