from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "sequence, name"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "type_id")
    sequence = fields.Integer(default=1, help="Used to order stages. Lower is better.")
    offer_ids = fields.One2many("estate.property.offer", "type_id")
    offer_count = fields.Integer(compute="_compute_offer_count")

    _check_name = models.Constraint(
        'unique(name)',
        'The type must be unique',
    )

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
