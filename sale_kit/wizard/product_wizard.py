from odoo import fields, models


class ProductWizard(models.TransientModel):
    _name = 'product.wizard'
    _description = 'Select the subproducts'

    product_id = fields.Many2one(comodel_name='product.product')
    quantity = fields.Integer()
    price = fields.Float()
    subproduct_id = fields.Many2one(comodel_name='subproduct.wizard')
