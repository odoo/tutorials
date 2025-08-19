from odoo import models, fields, api
from datetime import timedelta

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    price = fields.Float(string="Price")
    status = fields.Selection(
        string="Status",
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ]
    )
    validity = fields.Integer(
        string = "Validity (days)",
        default=7,
        help="Validity of the offer in days, after that it will be refused automatically."
    )
    date_deadline = fields.Date(
        string = "Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True,
    )
    partner_id = fields.Many2one("res.partner", string="Partner" , required=True)
    property_id = fields.Many2one("estate.property",string="Property", required=True)

    @api.depends('validity')
    def _compute_date_deadline(self):
        for offer in self:
            base_date = fields.Date.to_date(offer.create_date) if offer.create_date else fields.Date.context_today(offer)
            offer.date_deadline = base_date + timedelta(days=offer.validity or 0)

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.date_deadline:
                base_date = fields.Date.to_date(offer.create_date) if offer.create_date else fields.Date.context_today(offer)
                offer.validity = (offer.date_deadline - base_date).days
            else:
                offer.validity = 0


    # @api.onchange("date_deadline")
    # def _onchange_date_deadline(self):
    #     for offer in self:
    #         if offer.date_deadline:
    #             base_date = fields.Date.to_date(offer.create_date) if offer.create_date else fields.Date.context_today(offer)
    #             offer.validity = (offer.date_deadline - base_date).days
    #         else:
    #             offer.validity = 0