from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'
    _order = 'sequence'

    name = fields.Char('Name', required=True)
    sequence = fields.Integer('Sequence', default=1)

    property_ids = fields.One2many('estate.property', 'property_type_id')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer(compute='_count_offers')

    _unique_name = models.Constraint(
        'UNIQUE(name)',
        'Property type names should be unique'
    )

    def _count_offers(self):
        self.offer_count = len(self.offer_ids)


class EstatePropertyTypeLine(models.Model):
    _name = 'estate.property.type.line'
    _description = 'Estate Property Type Line'

    property_type_id = fields.Many2one('estate.property.type')
