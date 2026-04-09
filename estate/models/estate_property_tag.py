from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = "Property Tag"
    _order = "name"
    _check_unique_name = models.Constraint(
        'UNIQUE(name)',
        'The property tag name must be unique',
    )

    name = fields.Char(string="Name", required=True)
    color = fields.Integer(string="Color")
    
    tag_new = fields.One2many("estate.property","tag_ids",string="taglines")
    