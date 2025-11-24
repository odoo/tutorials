from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "sequence, name"

    name = fields.Char("Name", required=True)
    sequence = fields.Integer("Sequence")
    property_ids = fields.One2many(
        "estate.property", "property_type_id", string="Properties"
    )
    offer_count = fields.Integer(string="Offers count", compute="_compute_offer")
    offer_ids = fields.One2many(
        "estate.property.offer", "property_type_id", string="Offers"
    )

    # SQL constraints declared using the new API
    _unique_type_name = models.Constraint(
        'UNIQUE(name)', 'The property type name must be unique.'
    )

    @api.depends('offer_ids')
    def _compute_offer(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
