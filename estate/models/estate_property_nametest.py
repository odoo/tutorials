from odoo import fields, models


class EstatePropertyNametest(models.Model):
    _name = "estate.property.nametest"
    _description = "Real Estate Property Tag"
    _order = "name"

    name = fields.Char(string="Tag", required=True)
    _name_unique = models.Constraint(
        'unique(name)',
        '2 property tags cant be named the same string ',
    )
    property_ids = fields.Many2many("estate.property", string="properties")
    sequence = fields.Integer(string="sequence")
    color = fields.Integer()