from odoo import fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    uom_category_id = fields.Many2one(
        comodel_name='uom.uom',
        string='UoM Category',
        related='uom_id.category_id',
        store=True
    )

    pos_secondary_uom_id = fields.Many2one("uom.uom", string="POS Secondary Unit of Measure")

