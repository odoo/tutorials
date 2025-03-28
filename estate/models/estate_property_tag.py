from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate property tag'
    _order = 'name'
    _sql_constraints = [(
        'tag_name_unique', 'UNIQUE(name)',
        'Tag name should be unique.'
    )]

    name = fields.Char('Name', required=True)
    color = fields.Integer('Color', default=0)
