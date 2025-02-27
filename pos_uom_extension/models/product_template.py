from odoo import fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    uom_category_id = fields.Many2one('uom.category', string='UoM Category', related="uom_id.category_id")
    second_uom_id = fields.Many2one(
        'uom.uom',
        string="Second Uom",
        domain="[('category_id', '=', uom_category_id), ('id', '!=', uom_id)]",
        context={'create': False},
        help="Select an existing second UoM from the same category as the main UoM."
    )
