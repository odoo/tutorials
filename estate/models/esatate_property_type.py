# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class EstatePropertyTyeps(models.Model):
    _name = "estate.property.types"
    _description = "Types of Estate Property"
    _order = "sequence, name"
    _sql_constraints = [("_unique_type_name", "UNIQUE(name)", "Property type name must be unique.")]

    name = fields.Char(required=True, string="Title")
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
    sequence = fields.Integer(default=1, string="sequence")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers")
    offer_count = fields.Integer(string="Offer Count", compute="_compute_offer_count", store=True)

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
