from odoo import _, fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Real Estate Property Tag'

    name = fields.Char('Name', required=True)
    active = fields.Boolean('Active', default=True)

    _sql_constraints = [('unique_tag_name', 'UNIQUE(name)', _('Tag name should be unique.'))]
