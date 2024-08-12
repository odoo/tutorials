from odoo import models, fields, api


class EstatePropertyType(models.Model):

    _name = "estate.property.type"
    _description = "Estate property type"
    _order = 'name'

    name = fields.Char(string='Name', required=True)
    sequence = fields.Integer('Sequence', default=1)
    property_ids = fields.One2many(
        'estate.property', 'property_type_id', string="property")
    offer_ids = fields.One2many(
        comodel_name='estate.property.offer',
        inverse_name='property_type_id',
        string='Offers',
    )
    offer_count = fields.Integer(
        string='Offers Count',
        compute='_compute_offer_count',
        store=True
    )

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)',
         'THE PROPERTY TYPE NAME MUST BE UNIQUE ! ...')
    ]
