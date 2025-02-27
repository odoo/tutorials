# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class EstatePropertyAddOffer(models.TransientModel):
    _name = 'estate.property.add.offer'

    price = fields.Float(string="Price")
    validity = fields.Integer(string="Validity (days)", default=7)

    partner_id = fields.Many2one(comodel_name='res.partner', string="Partner", required=True)
    property_ids = fields.Many2many(comodel_name='estate.property', string="Properties")

    def action_add_offer(self):
        self.ensure_one()
        vals_list = []
        for property in self.property_ids:
            vals_list.append({
                'price': self.price,
                'validity': self.validity,
                'property_id': property.id,
                'partner_id': self.partner_id.id,
            })
        return self.env['estate.property.offer'].create(vals_list)
