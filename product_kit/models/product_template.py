from odoo import api,models,fields


class ProductTemplate(models.Model):
    _inherit = ['product.template']

    is_kit = fields.Boolean(default=False,string="Is Kit")   
    sub_product_ids = fields.Many2many('product.product', relation='sub_products_rel', column1='base_id', column2='sub_id')

    @api.onchange('is_kit')
    def _onchange_is_kit(self):

        if not self.is_kit:
            self.sub_product_ids=[(6,0,[])]
