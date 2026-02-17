from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tag describing a particular property characteristic"

    name = fields.Char(required=True)
