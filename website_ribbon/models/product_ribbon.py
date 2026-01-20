from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ProductRibbon(models.Model):
    _inherit = 'product.ribbon'

    style = fields.Selection([
        ('badge', 'Badge'),
        ('ribbon', 'Ribbon'),
    ], string="Style", default="ribbon", required=True)

    assign = fields.Selection([
        ('manual', 'Manually'),
        ('sale', 'Sale'),
        ('out_of_stock', 'Out of Stock'),
        ('new', 'New'),
    ], string="Assign", default="manual", required=True)

    days = fields.Integer(default=30)

    sequence = fields.Integer("Sequence", default=1)

    def _get_position_class(self):
        if self.style == 'badge':
            return 'o_tag_left' if self.position == 'left' else 'o_tag_right'
        return 'o_ribbon_left' if self.position == 'left' else 'o_ribbon_right'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            assign = vals.get('assign')
            if assign and assign != 'manual':
                if self.search_count([('assign', '=', assign)]) > 0:
                    raise ValidationError(
                        f"A ribbon with assign type '{assign}' already exists. You cannot create another one."
                    )
        return super().create(vals_list)

    def write(self, vals):
        assign = vals.get('assign')
        if assign and assign != 'manual':
            for ribbon in self:
                if self.search_count([('assign', '=', assign), ('id', '!=', ribbon.id)]) > 0:
                    raise ValidationError(
                        f"A ribbon with assign type '{assign}' already exists. You cannot assign another one."
                    )
        return super().write(vals)
