from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Estate Property Type"
    _order = 'sequence, name'
    _sql_constraints = [
        ('check_name_unique', 'UNIQUE(name)', 'The type name must be unique.'),
    ]

    name = fields.Char(required=True)
    property_ids = fields.One2many(
        'estate.property', 'property_type_id', string="Properties"
    )
    sequence = fields.Integer("Sequence", default=1)
    offer_count = fields.Integer(compute='_count_offers_compute', store=True)

    # Compute the total number of offers across all properties of this type
    @api.depends('property_ids.offer_ids')
    def _count_offers_compute(self):
        for record in self:
            record.offer_count = self.env['estate.property.offer'].search_count([
                ('property_id', 'in', record.property_ids.ids)
            ])
