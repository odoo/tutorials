from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Which type of property it is i.e apartment, house "

    name = fields.Char(required=True)
    