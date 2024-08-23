from odoo import models, fields


class estatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "tag for properties ..."

    name = fields.Char("Name", required=True)
