from odoo import api, models, fields
from datetime import date, timedelta
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"

    price = fields.Float()
    status = fields.Selection(
        [('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False
    )
    partner_id = fields.Many2one("res.partner", string="Customer", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True
    )

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Datetime.now()
            record.date_deadline = create_date.date() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Datetime.now()
            record.validity = (record.date_deadline - create_date.date()).days
            
    def action_accept(self):
     for offer in self:
        if offer.property_id.state == 'sold':
            raise UserError("Cannot accept an offer for a sold property.")
        
        # Refuse all other offers first
        other_offers = offer.property_id.offer_ids.filtered(lambda o: o.id != offer.id)
        other_offers.write({'status': 'refused'})

        # Accept current offer
        offer.status = 'accepted'
        offer.property_id.selling_price = offer.price
        offer.property_id.buyer = offer.partner_id
        offer.property_id.state = 'offer_accepted'


    def action_refuse(self):
        for offer in self:
            offer.status = 'refused'
    