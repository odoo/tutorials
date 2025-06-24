from odoo import api, fields, models


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "sequence, name"
    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         'The property type name must be unique.')
    ]

    # misc
    name = fields.Char(string='Type', required=True)
    sequence = fields.Integer(string='Sequence')

    # one2many
    property_ids = fields.One2many('estate.property',
                                   'property_type_id',
                                   string='Properties')
    offer_ids = fields.One2many('estate.property.offer',
                                'property_type_id',
                                string='Offers')

    # computed
    offer_count = fields.Integer(compute='_compute_offer_count',
                                 string='Offer Counts')

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
