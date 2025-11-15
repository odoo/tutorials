from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"
    _order = "name desc "
    color = fields.Integer(string='Color Index', default=3)

    name = fields.Char(required=True)
