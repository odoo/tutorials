from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "A property type is, for example, a house or an apartment. It is a standard business need to categorize properties according to their type, especially to refine filtering."

    name = fields.Char('Property type', required=True)
    _unique_name = models.Constraint(
        'unique (name)',
        'A property type name must be unique.'
    )
