from odoo import api, fields, models


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "describe the type property"
    _order = "sequence"

    sequence = fields.Integer('Sequence', default=1)

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_compute_nb_offer")

    # SQL constraints
    _sql_constraints = [
        ('name_unique', 'unique(name)',
         'The name of a property type should be unique')
    ]

    # Compute Methods
    @api.depends('offer_ids')
    def _compute_nb_offer(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
