from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate: Type of Property"

    name = fields.Char("Name", required=True)
    _sql_constraints = [("type_name_unique", "UNIQUE(name)", "A type with the same name already exists.")]
