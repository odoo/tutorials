from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Estate Property Type"
    _order = 'name'
    _sql_constraints = [
        ('unique_type_name', 'UNIQUE(name)', "Property type name must be unique.")
    ]

    name = fields.Char("Type", required=True)
    property_ids = fields.One2many('estate.property', "property_type_id")
    sequence = fields.Integer(
        'Sequence', default=1, help="Used to order stages. Lower is better."
    )
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer(compute='_compute_offer_count')

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
