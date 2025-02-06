from dateutil.relativedelta import relativedelta
from odoo import api, models, fields
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    # Offer Fields
    price = fields.Float(string="Price")
    status = fields.Selection(string="Status", copy=False, selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_deadline", inverse="_inverse_deadline")

    @api.depends('validity')
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + relativedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + relativedelta(days=record.validity)


    def _inverse_deadline(self):
        for record in self:
            if record.date_deadline:
                record.validity = (record.date_deadline - fields.Date.today()).days
            else:
                record.validity = 7
    
    # Action Button Methods
    def action_set_offer_status_accepted(self):
        for offer in self:
            if offer.status == 'accepted' or offer.status == 'refused':
                raise UserError("Property is already accepted or refused.")
            else:
                other_offers = self.env['estate.property.offer'].search([
                    ('property_id', '=', offer.property_id.id),
                    ('id', '!=', offer.id)  # Exclude the current offer
                ])

                other_offers.write({'status': 'refused'})

                offer.property_id.selling_price = offer.price
                offer.property_id.buyer = offer.partner_id

                offer.status = 'accepted'

    def action_set_offer_status_refused(self):
        for record in self:
            if record.status == 'accepted' or record.status == 'refused':
                raise UserError("Property is already accepted or refused.")
            else:
                self.status = 'refused'