import math

from odoo import models,fields,api


class MrpBomLine(models.Model):
    _inherit = ["mrp.bom.line"]

    diameter = fields.Float("DI")
    thickness = fields.Float("TH")
    length = fields.Float("LE")
    width = fields.Float("WI")
    product_qty = fields.Float(
        compute='_compute_product_qty',
        store=True
    )

    _sql_constraints = [
        ('check_diameter','CHECK(diameter > 0)','Diameter Price must be positive'),
        ('check_thickness','CHECK(thickness > 0)','Thickness Price must be positive'),
        ('check_length','CHECK(length > 0)','Length must be positive'),
        ('check_width','CHECK(width > 0)','Width must be positive'),
    ]

    @api.depends('diameter', 'width', 'length', 'thickness', 'product_id.specific_weight')
    def _compute_product_qty(self):
        for line in self:
            product_qt = 1
            if line.diameter and line.length:
                product_qt = max(product_qt,(
                    3.14159 * ((line.diameter ** 2) / 4) * line.length / 1000000
                ) * line.product_id.specific_weight)
            if line.length and line.width and line.thickness:
                product_qt = max(product_qt,(
                    (line.length * line.width * line.thickness / 1000000)
                ) * line.product_id.specific_weight)
            line.product_qty = math.floor(product_qt)
