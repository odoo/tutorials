from odoo import models, fields, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "this is defind the type of properties"
    _order = "name"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    sequence = fields.Integer(default=1)
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_compute_offer_count")

    _check_unique_type = models.Constraint("UNIQUE(name)", "The Type must be Unique")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        self.offer_count = len(self.offer_ids)
