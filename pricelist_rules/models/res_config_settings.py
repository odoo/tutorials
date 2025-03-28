# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    def set_values(self):
        super().set_values()
        products = self.env['product.template'].search([('is_pricelist_on', '!=', self.group_product_pricelist)])
        if products:
            products.write({'is_pricelist_on': self.group_product_pricelist})
