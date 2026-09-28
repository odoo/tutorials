from odoo import fields, models, api


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate property type"
    _order = "sequence, name"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id", "Property")
    sequence = fields.Integer("Sequence", default=1)
    offer_ids = fields.One2many(related="property_ids.offer_ids")
    offer_count = fields.Integer(compute="_compute_deadline")

    _uniq_name = models.Constraint(
        'UNIQUE(name)',
        "This type name is already taken"
    )

    @api.depends("offer_ids")
    def _compute_deadline(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
