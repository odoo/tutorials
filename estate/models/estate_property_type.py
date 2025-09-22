from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Real Estate Property Types"
    _order = 'name'

    name = fields.Char(required=True)
    sequence = fields.Integer(string='Sequence', default=1, help="Used to order stages. Lower is better.")

    property_ids = fields.One2many('estate.property', 'property_type_id', string="Properties")

    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string="Offers")
    offer_count = fields.Integer(compute='_compute_offer_count')

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    _check_unique_type = models.Constraint(
        'UNIQUE(name)',
        "The type name should be unique"
    )
