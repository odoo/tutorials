from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate properties Tags"

    name = fields.Char('Name', required=True, translate=True)
