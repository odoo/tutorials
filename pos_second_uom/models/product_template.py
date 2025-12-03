from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    pos_second_uom_id = fields.Many2one(
        'uom.uom',
        string="POS Second UoM",
        domain="[('category_id', '=', uom_category_id)]"
    )

    uom_category_id = fields.Many2one(
        'uom.category',
        string="UoM Category",
        related='uom_id.category_id',
    )

    @api.constrains('uom_id', 'pos_second_uom_id')
    def _check_secondary_uom_not_same_as_primary(self):
        if self.pos_second_uom_id and self.uom_id == self.pos_second_uom_id:
            raise ValidationError(
                f"Configuration Error:\n\n"
                f'Product "{self.name}" has "{self.uom_id.name}" set as both primary and secondary Unit of Measure.\n'
                f'These must be different. Please select a different second UoM for POS operations.'
            )
