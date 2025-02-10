from odoo import fields,models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate property Tags"

    name = fields.Char(string="Tag Name", required=True)
    
    # === SQL Constraints === #
    _sql_constraints = [
        ('unique_tag_name', 'UNIQUE(name)', 'All the tags must be unique')
    ]
