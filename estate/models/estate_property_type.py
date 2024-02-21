from odoo import fields, models


class EstateType(models.Model):
    _name = "estate.property.type"
    _description = "Properties types of estate."

    name = fields.Char(string="Name", required=True)

    _sql_constraints = [
        ('name_type_unique',
         'unique(name)',
         'The name of the type should be unique')]
