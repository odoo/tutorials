from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "this model defines property tags"

    name = fields.Char("Tag", required=True)
