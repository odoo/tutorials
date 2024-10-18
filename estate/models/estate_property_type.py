from odoo import api, fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "estate_property_type description"
    _sql_constraints = [
        ('check_type_name', 'unique(name)', 'A property type name must be unique.')
    ]
    _order = 'name'

    name = fields.Char(required=True)
    property_ids = fields.One2many(
        'estate.property',
        'property_type_id',
        string="Property"
    )
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    offer_ids = fields.One2many(
        'estate.property.offer',
        "property_type_id"
    )
    offer_count = fields.Integer(compute="_compute_offer_count")

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
