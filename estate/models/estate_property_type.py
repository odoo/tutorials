# licence

from odoo import fields
from odoo import models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Property type"

    name = fields.Char("Type", required=True, translate=True)
    description = fields.Text("Type description")
    # Constraints
    _sql_constraints = [
        ('check_name_unique', 'UNIQUE(name)',
         'The property type name must be unique'),
    ]
