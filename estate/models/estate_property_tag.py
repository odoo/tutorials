from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tags"
    _order = "name"
    _sql_constraints = [
        ('unique_tag_name', 'unique(name)', 'Tag name must be unique.')
    ]

    name = fields.Char(required=True, string="Tag")
    