from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Type of property for the estate module"
    _order = "sequence, name asc"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
    sequence = fields.Integer('Sequence', default=1, help="Used to order property types. Lower is better.")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_compute_offer_count")

    _name_param_uniq = models.Constraint(
        'UNIQUE (name)',
        'A property type name must be unique.'
    )

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
