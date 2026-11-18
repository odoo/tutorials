from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Type of property"
    _check_unique = models.UniqueIndex("(name)", "All property types need to have a unique name")

    name = fields.Char(required=True)
