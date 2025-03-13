# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class EstatePropertyOfferWizard(models.TransientModel):
    _name = 'estate.property.offer.wizard'
    _description = "Estate Property Offer Wizard"

    price = fields.Float(string="Price")
    partner_id = fields.Many2one(comodel_name='res.partner', string="Partner", required=True)
    property_id = fields.Many2one(comodel_name='estate.property', string="Property", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    @api.depends('validity')
    def _compute_date_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.date_deadline = fields.Date.add(offer.create_date, days=offer.validity)
            else:
                offer.date_deadline = fields.Date.add(fields.Date.today(), days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            offer.validity = (offer.date_deadline - fields.Date.to_date(offer.create_date)).days

    @api.model_create_multi
    def create(self, vals_list):
        for offer in vals_list:
            active_id = self.env.context.get('active_id')
            offer['property_id'] = active_id
            self.env['estate.property.offer'].create(offer)
        return super().create(vals_list)
