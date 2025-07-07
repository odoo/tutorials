from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name="estate.property.tag"
    _description="Tags For Estate Properties"

    name = fields.Char(required=True, string="Tag")