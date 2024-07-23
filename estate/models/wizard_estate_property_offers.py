from odoo import models, fields, api
from dateutil.relativedelta import relativedelta


class WizardOffers(models.TransientModel):
    _name = 'wizard.offer'
    _description = 'Wizard for Estate Property Offers'

    price = fields.Float(string='Offer Price', required=True)
    partner_id = fields.Many2one('res.partner', string='Buyer', required=True)
    validity = fields.Integer("Validity (Days)", default=7)
    date_deadline = fields.Date("Deadline", compute="_deadline_date_count", inverse="_inverse_deadline", store=True, required=True, default=lambda self: fields.Datetime.now() + relativedelta(days=7))

    @api.depends('validity')
    def _deadline_date_count(self):
        current_date = fields.Date.today()
        for record in self:
            record.date_deadline = current_date + relativedelta(days=record.validity)

    def _inverse_deadline(self):
        current_date = fields.Date.today()
        for record in self:
            record.validity = relativedelta(record.date_deadline, current_date).days

    def action_add_offer(self):
        active_ids = self.env.context.get('active_ids', [])
        properties = self.env['estate.property'].browse(active_ids)
        for record in properties:
            self.env['estate.property.offer'].create({
                'property_id': record.id,
                'partner_id': self.partner_id.id,
                'price': self.price,
                'date_deadline': self.date_deadline,
            })
        return {'type': 'ir.actions.act_window_close'}
