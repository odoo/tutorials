from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Estate property type"

    _order = 'sequence asc'

    name = fields.Char(required=True, string="Title")
    property_ids = fields.One2many('estate.property', 'property_type_id', string="Properties")
    sequence = fields.Integer()
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string="Offers")
    offer_count = fields.Integer(compute='_compute_offer_count')

    _name_unique_idx = models.UniqueIndex(
        '(name)',
        "The title of the property type must be unique."
    )

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    def action_show_offers(self):
        self.ensure_one()

        return {
            'name': self.env._("Offers"),
            'view_mode': 'list,form',
            'res_model': 'estate.property.offer',
            'type': 'ir.actions.act_window',
            'context': {'create': False, 'delete': False, 'edit': False},
            'domain': [('property_type_id', 'in', self.id)],
            'target': 'current',
        }
