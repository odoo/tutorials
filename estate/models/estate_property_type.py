from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "name"
    _name_unique = models.Constraint("unique (name)", "Ce type de propriété existe déjà.")

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
