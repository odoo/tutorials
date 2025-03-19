from odoo import models, fields

class estatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"
    _order="name"

    name = fields.Char("Name", required=True)
    color = fields.Integer("Color", default=0)

    _sql_constraints = [
        ("check_tag_ids", "UNIQUE(name)", "Property Tag name must be unique")
    ]