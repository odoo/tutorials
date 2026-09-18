from odoo import models, fields, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property types of the estate"
    _order = "sequence, name"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id", copy=False)
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", copy=False)
    offer_count = fields.Integer(compute="_compute_offer_count", store=True)

    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")

    _name_uniq = models.Constraint(
        'unique(name)',
        'The name must be unique.',
    )

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
