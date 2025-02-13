from odoo import api, fields, models


class EstatePropertyType(models.Model):

    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "name"
    _sql_constraints = [
        (
            "check_unique_estate_property_type",
            "unique(name)",
            "This Property Type already exists",
        )
    ]
    # --------------------------------------- Fields Declaration ----------------------------------
    # Basic Fields
    name = fields.Char(string="Type", required=True)
    sequence = fields.Integer(string="sequence", default="1")
    # Relational view
    property_ids = fields.One2many("estate.property", "property_type_id")
    # stat button method
    offer_ids = fields.One2many("estate.property.offer", inverse_name="property_type_id", string="Offers")
    offer_count = fields.Integer(string="Offers Count", compute="_compute_offer_count")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
