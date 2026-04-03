from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real estate system - Property Type"

    _check_type_name = models.Constraint(
        'UNIQUE(name)',
        'The Property Type name has to be Unique.'
    )

    name = fields.Char(string="Property Type Name", required=True)
