from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate_property_tag_model"
    _description = "This is a property tag model"
    _order = "name"

    name = fields.Char(required=True)
    Color = fields.Integer(string="color")
    # property_name = fields.Many2many("estate_property_tag_model", "tag_ids")

    _sql_constraints = [
        ("check_tag_name", "UNIQUE(name)", "tag name should be unique")
    ]