from odoo import models, fields, api

class EstatePropertyType(models.Model):

    _name = "estate.property.type"
    _description = "type of estate property"
    _sql_constraints = [
        ("unique_type_name", "UNIQUE(name)","The type name should be unique.")
    ]
    _order = "name asc"

    name = fields.Char(required=True)
    property_ids = fields.One2many(comodel_name="estate.property", inverse_name="property_type_id")
    offer_ids = fields.One2many(comodel_name="estate.property.offer", inverse_name="property_type_id")
    offer_count = fields.Integer(compute="_compute_offer_count")


    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)