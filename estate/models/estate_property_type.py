from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "estate property type"
    _order = "sequence"

    _check_type_name = models.Constraint(
        "UNIQUE(name)",
        "The property type name must be unique.",
    )

    name = fields.Char(string="Title", required=True)
    property_ids = fields.One2many("estate.property", "property_type_id", string="Property")
    sequence = fields.Integer(string="Sequence", default=1)
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="offers")
    offer_count = fields.Integer(string="offer count", default=0, compute="_compute_offer_count")

    @api.onchange('offer_ids')
    def _compute_offer_count(self):
        for property_type in self:
            property_type.offer_count = len(property_type.offer_ids)

    def action_open_linked_offers(self):
        self.ensure_one()
        return {
            'name': self.name,
            'view_mode': 'list,form',
            'res_model': 'estate.property.offer',
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', self.offer_ids.ids)],
        }
