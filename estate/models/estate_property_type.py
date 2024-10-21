from odoo import api, fields, models #type: ignore


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _order = "sequence, name"  # Default order by sequence then name
    sequence = fields.Integer(string="Sequence", default=10)

    _sql_constraints = [
        ('unique_type_name', 'UNIQUE(name)', 'Property type name must be unique.'),
        ]
    
    _description = 'Property Type'

    name = fields.Char(required=True)
    property_ids = fields.One2many(
        'estate.property',
        'property_type_id',
        string="Properties"
    )

    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string="Offers")
    offer_count = fields.Integer(compute='_compute_offer_count', string="Number of Offers")

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
            