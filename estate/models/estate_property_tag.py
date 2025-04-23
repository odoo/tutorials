from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate property tag description"

    name = fields.Char('name', required=True)
