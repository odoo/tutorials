from odoo import api, models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Type of properties"
    _order = "name asc"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    sequence = fields.Integer('Sequence', default=1)
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_compute_count_offer")

    _unique_type = models.Constraint(
        'unique(name)',
        'The type name must be unique',
    )

    @api.depends("offer_ids")
    def _compute_count_offer(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
