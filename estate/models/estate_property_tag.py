from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate_property.tag"
    _description = "Tag of Estate Property"
    _order = "name"

    color = fields.Integer()

    name = fields.Char('Nom', required=True)
