from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate property type"
    _order = "name"

    name = fields.Char(required=True)
    sequence = fields.Integer('Sequence', default=1)
    property_ids = fields.One2many("estate.property", "property_type_id")

    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', store=True)

    offer_count = fields.Integer(compute='_compute_offer_count')

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    _sql_constraints = [
        ('check_name', 'unique(name)',
         'This type already exists.') 
    ]

class EstatePropertyTypeLine(models.Model):
    _name = "estate.property.type.line"
    _description = "Estate property type line"

    property_id = fields.Many2one("estate.property")
    name = fields.Char()
    expected_price = fields.Float()
    state = fields.Char()
