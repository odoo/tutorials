"""module for the estate property type model"""

from odoo import api, fields, models

class EstatePropertyType(models.Model):
    "Estate property type odoo model"
    _name = "estate.property.type"
    _description= "real estate asset types (e.g. house)"
    _order = "sequence, name"
    _sql_constraints = [("unique_name", "UNIQUE(name)", "property type names must be unique")]

    sequence = fields.Integer("Sequence")
    name = fields.Char("Name", required = True)
    property_ids = fields.One2many("estate.property", "type_id")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_compute_offer_count")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for rec in self:
            rec.offer_count = len(rec.offer_ids)
