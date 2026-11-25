from odoo import api, fields, models


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Type"
    _order = 'name'

    name = fields.Char('Name', required=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order properties.")
    property_ids = fields.One2many('estate.property', 'property_type_id')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer(string='# Offers', compute='_compute_offer_count')

    _check_name_uniq = models.Constraint(
        'UNIQUE (name)',
        "This type of property already exists.",
    )

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
