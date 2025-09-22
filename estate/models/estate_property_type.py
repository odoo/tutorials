from odoo import api, fields, models


class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Test description for estate.property.type model"
    _order = 'name'

    name = fields.Char(required=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order types.")
    property_ids = fields.One2many('estate.property', 'property_type_id', string="Properties")
    offers_ids = fields.One2many('estate.property.offer', 'property_type_id', string="Offers")
    offer_count = fields.Integer(compute='_compute_offer_count', default=0)

    _check_name = models.Constraint(
        'UNIQUE (name)',
        "Property type name must be unique",
    )

    @api.depends('offers_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offers_ids or [])
