from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tags"

    _order = "name"

    name = fields.Char(string="Tag Name")

    color = fields.Integer()

    # -------------------------------------------------------------------------
    # SQL CONSTRAINTS QUERIES
    # -------------------------------------------------------------------------

    _sql_constraints = [
        ('unique_tag_name', 'UNIQUE(name)', 'The property tag name must be unique.')
    ]
