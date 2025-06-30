from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name asc"

    name = fields.Char("Name", required=True)
    color = fields.Integer("Color Index", help="Color index for the tag in the Kanban view")
    
    