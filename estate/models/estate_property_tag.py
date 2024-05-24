from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "estate property tags"
    name = fields.Char('Tag Name', required=True)