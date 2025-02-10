from odoo import fields, models


class EstatePropertyType(models.Model):

    _name = "estate.property.type"
    _description = "Real Estate Property Type"

    # --------------------------------------- Fields Declaration ----------------------------------

    # Basic Fields    
    name = fields.Char(string="Type", required=True)
    # Relational view
    property_ids = fields.One2many("estate.property","property_type_id")
    