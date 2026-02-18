from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "This is my second model"
    _order = "sequence, name"

    name = fields.Char(required=True)
    sequence = fields.Integer()
    offer_count = fields.Integer(compute="_compute_offer_count")

    property_ids = fields.One2many('estate.property', 'property_type_id', string="Properties")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers")

    _unique_name = models.Constraint(
        'UNIQUE(name)',
        'The name of the type must be unique!',
    )

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
