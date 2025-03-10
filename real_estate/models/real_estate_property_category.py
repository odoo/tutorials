from odoo import fields, models, api

class RealEstateCategory(models.Model):
    _name = "real.estate.property.category"
    _description = "Table for Categories of properties"
    _order = "sequence, name"

    name = fields.Char(string = 'Category', required = True)
    sequence = fields.Integer('Sequence', default=1)
    property_ids = fields.One2many('real.estate.property', 'property_type_id')
    offer_ids = fields.One2many('real.estate.property.offer', 'property_type_id')
    offer_count = fields.Integer(compute = '_compute_offer_count', string = 'Total Offers')

    #Adding Sql constraints to tag name for unique tag name
    _sql_constraints = [
        ('check_type_name', 'UNIQUE(name)', 'A property type name must be unique')
    ]

    # Count total offers
    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids.mapped(id))
