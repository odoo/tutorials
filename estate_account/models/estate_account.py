from odoo import models, fields

class EstateAccount(models.Model):
    _name = "estacc.main"
    _description = "estacc stuff"

    _check_name = models.Constraint(
        'unique(name)',
        'There is already a property tag with that name!',
    )

    name = fields.Char(required=True)
