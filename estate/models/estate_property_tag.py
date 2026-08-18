from odoo import models, fields


class EstatePropertyTag(models.Model):

    _name = "estate.property.tag"
    _description = "Estate property tag"

    name = fields.Char("Property Tag Name", required=True)
