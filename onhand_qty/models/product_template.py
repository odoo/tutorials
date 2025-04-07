from odoo import fields, api, models


class product_template(models.Model):
    _inherit = "product.template"

    qty_input = fields.Float(
        string="Quantity On Hand ",
        compute='_compute_qty_input',
        inverse='_inverse_qty_input',
        store=True,
    )

    is_multi_location = fields.Boolean(
        compute="_compute_is_multi_location", store=False
    )

    @api.depends('qty_available')
    def _compute_qty_input(self):
        for rec in self:
            rec.qty_input = rec.qty_available

    @api.depends("company_id")
    def _compute_is_multi_location(self):
        for product in self:
            product.is_multi_location = self.env.user.has_group(
                "stock.group_stock_multi_locations"
            )

    @api.onchange('qty_input')
    def _onchange_qty_input(self):
        for product in self:
            quant = self.env['stock.quant'].sudo().search([
                ('product_id', '=', product.product_variant_id.id),
                ('location_id.usage', '=', 'internal')
            ], limit=1)

            if quant:
                quant.quantity = product.qty_input
            else:
                self.env['stock.quant'].sudo().create({
                    'product_id': product.product_variant_id.id,
                    'location_id': 8,
                    'quantity': product.qty_input,
                })

    def _inverse_qty_input(self):
        pass
