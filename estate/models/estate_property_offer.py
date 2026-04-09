from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property offer'

    price = fields.Float()
    status = fields.Selection(
        [
            ('accepted', "Accepted"),
            ('refused', "Refused")
        ],
        copy=False)

    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(string="Validity (Days)", default=7)
    date_deadline = fields.Date(string="Date Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True)

    _check_price = models.Constraint(
        'CHECK(price > 0)',
        'Offer price must be  positive.'
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            starting_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = starting_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            starting_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.validity = (record.date_deadline - starting_date).days

    def action_accept(self):
        for record in self:
            already_accepted = False
            for offer in record.property_id.offer_ids:
                if offer.status == 'accepted':
                    already_accepted = True
            if already_accepted:
                raise UserError("Only one offer can be accepted")
            record.status = 'accepted'
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
        return True

    def action_refuse(self):
        for record in self:
            record.status = "refused"
        return True
