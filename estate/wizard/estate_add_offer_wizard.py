from dateutil.relativedelta import relativedelta
from odoo import fields, models


class AddOfferWizard(models.TransientModel):
    _name = "estate.add.offer.wizard"
    _description = 'Create Offer On Multiple Properties'

    partner_id = fields.Many2one("res.partner", string="Buyer")
    price = fields.Float('Price')
    date_deadline = fields.Date('Deadline', default=fields.Datetime.today() + relativedelta(days=7))

    def action_on_add_offer(self):
        for prop in self._context.get('active_ids'):
            self.env['estate.property.offer'].create({
                "property_id": prop,
                "partner_id": self.partner_id.id,
                "price": self.price,
                "date_deadline": self.date_deadline
            })
