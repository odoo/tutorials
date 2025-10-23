from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name"
    _name_unique = models.Constraint("unique (name)", "Ce tag existe déjà.")

    name = fields.Char(required=True)
    color = fields.Integer()
