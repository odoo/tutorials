from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Define a type of property"
    _order = "sequence, name"

    name = fields.Char(required=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order property types. Lower is better.")

    property_ids = fields.One2many('estate.property', 'property_type_id')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')

    offer_count = fields.Integer(string="Offers", compute='_compute_offer_count')

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    _check_unique_name = models.Constraint(
        'UNIQUE (name)',
        'The property type name must be unique.',
    )
