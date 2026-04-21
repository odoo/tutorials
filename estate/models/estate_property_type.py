# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"
    _order = "name"

    _check_name_unique = models.Constraint(
        "UNIQUE(name)", "The property type name must be unique."
    )

    name = fields.Char(required=True)
    property_ids = fields.One2many(
        "estate.property", "estate_type_id", string="Properties"
    )
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_compute_offer_count")
    sequence = fields.Integer(
        "Sequence", default=1, help="Used to order stages. Lower is better."
    )

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
