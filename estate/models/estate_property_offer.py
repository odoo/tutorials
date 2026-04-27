from odoo import api, fields, models, exceptions
from datetime import timedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    price = fields.Float("Price")
    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer("Validity (days)", default=7)

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for offer in self:
            if offer.validity:
                if offer.create_date:
                    offer.date_deadline = offer.create_date + timedelta(days=offer.validity)
                else:
                    offer.date_deadline = fields.Date.today() + timedelta(days=offer.validity)
            else:
                offer.date_deadline = False

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.date_deadline:
                if offer.create_date:
                    offer.validity = offer.date_deadline.day - offer.create_date.day
                else:
                    offer.validity = (offer.date_deadline - fields.Date.today()).day
            else:
                offer.validity = 0

    date_deadline = fields.Date("Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True)

    def action_accept(self):
        for offer in self:
            existing_accepted = self.env['estate.property.offer'].search([
                ('property_id', '=', offer.property_id.id),
                ('status', '=', 'accepted')
            ])
            if existing_accepted:
                raise exceptions.UserError("An offer for this property has already been accepted.")
            offer.status = 'accepted'

    def action_refuse(self):
        for offer in self:
            offer.status = 'refused'
