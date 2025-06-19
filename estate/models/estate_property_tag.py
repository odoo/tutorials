from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Store Real Estate Properties Tags"

    name = fields.Char("Estate Type Tag", required=True, translate=True)

    # SQL Constraints
    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'The tag must be unique.')
    ]