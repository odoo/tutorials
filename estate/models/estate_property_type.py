from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate property type, i.e. type of the building accourding to the use"

    name = fields.Char(required=True)
    description = fields.Text(help="Description of thus estate property type for better user understanding")
    code = fields.Char(required=True, help="Single to double character code for identification when space is scarce")
