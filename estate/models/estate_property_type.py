from odoo import api, fields, models

class estatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "sequence, name"

    name = fields.Char(required=True)
    sequence = fields.Integer(default=1)
    # Add the One2many field to store the related properties
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
    offer_ids = fields.One2many(
        "estate.property.offer", "property_type_id", string="Offers"
    )
    offer_count = fields.Integer(
        string="Offer Count",
        compute="_compute_offer_count", store=True
    )
    
    #constraint
    _sql_constraints = [
        ("unique_property_type_name", "UNIQUE(name)", "The property type name must be unique."),
    ]

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)  
