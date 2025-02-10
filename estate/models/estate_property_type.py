# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Contains all property type"
    _order = "sequence, name"

    name = fields.Char(string="Property Type", required=True)
    sequence = fields.Integer(string="Sequence")

    offer_count = fields.Integer(string="Offer Count", compute="_compute_offer_count")

    property_ids = fields.One2many(string="Properties", comodel_name="estate.property", inverse_name="property_type_id")
    offer_ids = fields.One2many(string="Offers", comodel_name="estate.property.offer", inverse_name="property_type_id")

    _sql_constraints = [("name_uniq", "unique(name)", "Property Type already exists")]

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
