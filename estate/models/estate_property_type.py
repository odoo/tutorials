from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate_property_type"
    _description = "this is defind the type of properties"

    name = fields.Char(required=True)
    property_ids=fields.One2many('estate_property','property_type_id')
    _check_unique_type = models.Constraint("UNIQUE(name)", "The Type must be Unique")
