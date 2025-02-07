from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name"
    
    _sql_constraints=[
        (
            'unique_property_tag', 'UNIQUE(name)', 'Tag with this name already exists'
        )
    ]
    
    name = fields.Char(string="Name", required=True)
    active = fields.Boolean(default=True)
    color = fields.Integer(string="Color")
