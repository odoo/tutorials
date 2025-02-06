from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"
    _order = "name asc"

    name = fields.Char(string="Tag Name", required=True)
    # color = fields.Integer(string="color")