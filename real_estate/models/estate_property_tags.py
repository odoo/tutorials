from odoo import fields, models


class EstatePropertyTags(models.Model):
    _name = "estate.property.tags"
    _description = "Real Estate Property Tags"
    _order = "name asc"

    name = fields.Char(string="Name", required=True)
    color = fields.Integer(string="Color")

    _name_uniq = models.Constraint('unique (name)', "This tag is already available")
