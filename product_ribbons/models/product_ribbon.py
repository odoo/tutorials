from odoo import  api, fields, models
from odoo.exceptions import ValidationError


class ProductRibbon(models.Model):
    _inherit = "product.ribbon"

    style = fields.Selection(
        [("badge", "Badge"), ("ribbon", "Ribbon")],
        string="Style",
        default="ribbon",
        required=True,
    )
    assign = fields.Selection(
        [
            ("manual", "Manual"),
            ("sale", "Sale"),
            ("out_of_stock", "Out of Stock"),
            ("new", "New"),
        ],
        string="Assign",
        default="manual",
        required=True,
    )
    show_period = fields.Integer(default=30)

    def _get_position_class(self):
        if self.style == 'ribbon':
            return 'o_ribbon_left' if self.position == 'left' else 'o_ribbon_right'
        else:  # self.style == 'badge'
            return 'o_tag_left' if self.position == 'left' else 'o_tag_right'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            assign_type = vals.get('assign')
            if assign_type and assign_type != 'manual':
                existing_ribbon = self.search([('assign', '=', assign_type)], limit=1)
                if existing_ribbon:
                    raise ValidationError(f"A ribbon with assign type '{assign_type}' already exists. You cannot create another one.")
        return super().create(vals_list)
        
    def write(self, vals):
        assign_type = vals.get('assign')
        if assign_type != 'manual':
            existing_ribbon = self.search([('assign', '=', assign_type), ('id', '!=', self.id)])
            if existing_ribbon:
                raise ValidationError(f"A ribbon with assign type '{assign_type}' already exists. You cannot assign another one.")
        return super().write(vals)
