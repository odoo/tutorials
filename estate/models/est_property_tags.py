from odoo import models, fields

class EstateTag(models.Model):
    _name = "est.property.tag"
    _description = "Property tags"
    _order = "name asc"

    _check_name = models.Constraint(
        'unique(name)',
        'There is already a property tag with that name!',
    )

    name = fields.Char("name", required=True)
    color = fields.Integer("color")
