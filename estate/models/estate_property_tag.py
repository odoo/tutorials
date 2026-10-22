
from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate_property_tag"
    _description = "Estate Property Tag"
    _order = "name"

    name = fields.Char('Name', required=True, translate=True)
    _unique_name = models.Constraint("UNIQUE(name)", "Tag name must be unique.")
    description = fields.Text('Description')
    active = fields.Boolean('Active', default=True)
    sequence = fields.Integer('Sequence', default=10)
    color = fields.Integer('Color')
    _valid_color = models.Constraint("CHECK(color >= 0 AND color <= 11)", "Color must be a valid Color ID between 0 and 11.")
