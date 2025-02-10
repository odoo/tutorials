# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _sql_constraints = [
        ("unique_type_name", "UNIQUE(name)", "Property type name must be unique."),
    ]
    _order = "sequence, name"

    name = fields.Char(string="Property Type", required=True)
    property_ids = fields.One2many(
        "estate.property", 
        "property_type_id", 
        string="Properties", 
        required=True
    )
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers")
    offer_count = fields.Integer(compute="_compute_offer_count", string="Offer Count")
    sequence = fields.Integer('Sequence', default=1, help="Used to manually order properties")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
