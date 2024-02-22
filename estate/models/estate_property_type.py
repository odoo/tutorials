from odoo import fields, models


class EstateType(models.Model):
    _name = "estate.property.type"
    _description = "Properties types of estate."
    _order = "sequence,name asc"

    name = fields.Char(string="Name", required=True)
    property_ids = fields.One2many("estate.property", "property_type_id", string="Property")
    sequence = fields.Integer('Sequence', default=1, help="Index to order.")

    _sql_constraints = [
        ('name_type_unique',
         'unique(name)',
         'The name of the type should be unique')]
