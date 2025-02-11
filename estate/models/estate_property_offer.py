from odoo import api, fields, models
from datetime import timedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Offer Property Model"

    price = fields.Float("Price")
    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('rejected', 'Rejected')
        ],
        copy=False
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer("Validity", default=7)
    date_deadline = fields.Date("Deadline", compute="_compute_deadline_date", inverse="_inverse_deadline_date")

    def action_accept_offer(self):
        for record in self:
            record.status = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.state = 'offer_accepted'
            record.property_id.buyer = record.partner_id
            rejected_offers = self.search([
                ('property_id', '=', record.property_id.id), ('id', '!=', record.id)
            ])
            rejected_offers.write({'status':'rejected'})

    def action_reject_offer(self):
        for offer in self:
            offer.status = 'rejected'

    @api.depends("create_date","validity")
    def _compute_deadline_date(self):
        for record in self:
            create_date = record.create_date or fields.Date.today()
            record.date_deadline = create_date + timedelta(days=record.validity)

    def _inverse_deadline_date(self):
        for record in self:
            if record.create_date and record.date_deadline:
                record.validity = (record.date_deadline - record.create_date.date()).days
            else:
                record.validity = 7
