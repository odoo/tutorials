from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Type"
    _order = "sequence, name"

    name = fields.Char(required=True)
    sequence = fields.Integer('Sequence', default=1)
    property_ids = fields.One2many('estate.property', 'property_type_id', string="Properties")
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string="Offers")
    offer_count = fields.Integer(compute="_compute_offer_count")

    _sql_constraints = [
        ('check_name', 'UNIQUE(name)', 'The name must be unique.'),
    ]

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for type in self:
            type.offer_count = len(type.offer_ids)

    @api.ondelete(at_uninstall=False)
    def _unlink_except_property_new_cancelled(self):
        for property in self:
            if not property.state in ('new', 'cancelled'):
                raise UserError("Only new and cancelled properties can be deleted.")

        return super().unlink()
