from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tags describing the property such as 'cozy' and 'renovated'"

    name = fields.Char(required=True)
