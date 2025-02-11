from odoo import fields, models, api # type: ignore

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _sql_constraints = [
        ('check_unique_property_type', 'UNIQUE(name)', 'Property Type already exists')
    ]

#---------------------------------------Basic Fields---------------------------------------#
    name = fields.Char("Name", required=True)

#---------------------------------------Relational Fields----------------------------------#
    property_ids = fields.One2many("estate.property","property_type_id",string="Properties")
    