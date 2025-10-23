from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = 'sequence, name, id'

    name = fields.Char('Type', required=True)
    description = fields.Text()
    property_ids = fields.One2many('estate.property', 'property_type_id')
    sequence = fields.Integer('Sequence', default=1)
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer(compute="_computer_offers_count")

    _unique_type = models.Constraint(
        'UNIQUE(name)',
        'Property type name exists'
    )

    @api.depends("offer_ids")
    def _compute_offers_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)