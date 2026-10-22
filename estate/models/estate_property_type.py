from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Type of property for the estate module"
    _order = "name"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    offer_ids = fields.One2many(related="property_ids.offer_ids")
    offer_count = fields.Integer(compute="_compute_offer_count", default=0)

    _name_param_uniq = models.Constraint(
        'UNIQUE (name)',
        'A property selling price must be positive'
    )

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
