from odoo import models, fields


class EstatePropertyTag(models.Model):

    _name = "estate.property.tag"
    _description = "estate property tag description"

    name = fields.Char('Name', required=True)
