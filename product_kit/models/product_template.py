from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    isKit = fields.Boolean(string="is Kit", default=False)
    subProduct = fields.Many2many('product.product', string="Sub Products")
    subProductVisibility = fields.Boolean(string="is Kit", default=False, compute='_compute_sub_product_visiblity')

    @api.depends_context('isKit')
    def _compute_sub_product_visiblity(self):
        if self.isKit:
            self.subProductVisibility = True
        else:
            self.subProductVisibility = False
