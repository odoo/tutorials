from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    deposit_product_id = fields.Many2one("product.product", string="Deposit Product", help="Product to be used for deposit on sale order.")

    def set_values(self):
        super().set_values()
        self.env['ir.config_parameter'].sudo().set_param('deposit_product_id', self.deposit_product_id.id)

    def get_values(self):
        res = super().get_values()
        product_id = int(self.env['ir.config_parameter'].sudo().get_param('deposit_product_id', default=False))
        res['deposit_product_id'] = self.env['product.product'].browse(product_id)
        return res
