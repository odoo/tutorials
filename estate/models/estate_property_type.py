from odoo import models, fields

class EstatePropertyType(models.Model):

    _name = "estate.property.types"
    _description = "Different kind of estate properties"

    name = fields.Char(name = "Type of Estate Property", required = True)
