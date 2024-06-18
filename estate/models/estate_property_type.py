from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"
    _order = "name"
    _sql_constraints = [
        ('check_unique_name', 'unique (name)', 'All property type must be unique'),
    ]
    
    name = fields.Char(required=True, string="Type")
    property_ids = fields.One2many("estate.property", "property_type_id", "Properties")
    sequence = fields.Integer("Sequence")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_compute_offer_count")

    @api.depends("offer_ids")
    def _compute_offer_count(self) -> None:
        for property_type in self:
            property_type.offer_count = len(property_type.offer_ids)