from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"

    name = fields.Char(string="Type", required=True)

     # ch-11 ex-3, ex-4
    _order = "sequence, name"

    # chapter-11 exercise-1
    property_ids = fields.One2many("estate.property","property_type_id", string="Properties")

    # ch-11 ex-4
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")