from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"

    name = fields.Char(required=True)
    _order = "name"
    color = fields.Integer(string = "Color")
    tag_ids = fields.Many2many(
        'estate.property.tag',
        'estate_property_tag_rel',  
        'tag_id1',  
        'tag_id2',
        string="Related Tags"
    )
    _sql_constraints = [
        ("check_name", "UNIQUE(name)", "The property tag must be unique")
    ]
