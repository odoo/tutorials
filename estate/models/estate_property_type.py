from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'
    _order = 'sequence, name'

    name = fields.Char('Property Type', required=True)
    sequence = fields.Integer('Sequence', default=10)
    property_ids = fields.One2many('estate.property', 'property_type_id', string="Properties")
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string="Offers")
    offer_count = fields.Integer(compute='_compute_offer_count', string='Offers Count')

    _sql_constraints = [
        ('check_property_type', 'UNIQUE(name)', 'The Property type should be unique')]

    # Count number of offer related to property type
    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
