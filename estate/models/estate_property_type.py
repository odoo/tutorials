from odoo import models, fields, api


class EstateProperty(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'
    _order = 'sequence, name'

    name = fields.Char(string="Name", required=True)
    sequence = fields.Integer(string='Sequence', default=10)
    property_ids = fields.One2many('estate.property', 'property_type_id', string="Properties")
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string="Offers")
    offer_count = fields.Integer(
        string="Number of Offers",
        compute='_compute_offer_count'
    )

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'This property type already exists.'),
    ]

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
