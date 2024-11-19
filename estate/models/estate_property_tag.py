from odoo import fields, models, _


class EstatePropertyTagModel(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer()

    _sql_constraints = [
        ('check_unique_name', 'unique(name)',
         _('Tag name must be unique.')),
    ]
