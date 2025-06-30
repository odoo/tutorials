from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real estate properties types"
    _order = "sequence, name"

    name = fields.Char("Name", required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id')
    sequence = fields.Integer("Sequence", default=1, help="Used to order stages. Lower is better.")

    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer(compute='_compute_count')

    _sql_constraints = [
        ('name_unique', 'unique (name)', 'Each name must be unique.'),
    ]

    @api.depends('offer_ids')
    def _compute_count(self):
        self.offer_count = len(self.offer_ids)

    def go_to_offer_button(self):
        return True
