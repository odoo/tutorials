from odoo import models, fields


class estatePropertyTag(models.Model):
    
    _name = "estate.property.tag"
    _description = "This is property Tag model"
    _order = "name"

    name = fields.Char(required=True, string="Tag")
    active = fields.Boolean(required=True)
    color = fields.Integer(default=12)

    _sql_constraints = [
            ('check_unique_tag_name','UNIQUE(name)','This tag is already exists.')
    ]
