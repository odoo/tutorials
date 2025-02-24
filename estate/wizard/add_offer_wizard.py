# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class AddOfferWizard(models.TransientModel):
    _name = 'add.offer.wizard'

    price = fields.Float(string="Price")
    validity = fields.Integer(string="Validity (days)", default=7)

    partner_id = fields.Many2one(comodel_name='res.partner', string="Partner", required=True)
    property_ids = fields.Many2many(comodel_name='estate.property', string="Properties")

    def action_add_offer(self):
        self.ensure_one()
        for property in self.property_ids:
            self.env['estate.property.offer'].create({
                'price': self.price,
                'validity': self.validity,
                'property_id': property.id,
                'partner_id': self.partner_id.id,
            })
        return
