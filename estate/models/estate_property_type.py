from odoo import models, fields, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate properties Types"
    _order = "name"
    name = fields.Char('Name', required=True, translate=True)
    properties_ids = fields.One2many("estate.property", "property_type_id", "Properties")
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    offers_ids = fields.One2many("estate.property.offer", "property_type_id", "Offers")
    offers_count = fields.Integer(compute='_compute_offers_count')
    _types_uniq = models.Constraint(
        'unique(name)',
        "The type name already exists",
    )

    @api.depends('offers_ids')
    def _compute_offers_count(self):
        for record in self:
            record.offers_count = len(record.offers_ids)
