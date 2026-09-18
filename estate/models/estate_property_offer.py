from datetime import datetime

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class EstatePropertyOfferModel(models.Model):
    _name = "estate_property_offer"
    _description = "An offer for an estate"

    price = fields.Float()
    status = fields.Selection(string='State',
            selection=[
                ('refused', 'Refused'),
                ('accepted', 'Offer Accepted'),
            ],
            copy=False,
        )
    partner_id = fields.Many2one("res.partner", string="Buyer")
    property_id = fields.Many2one("estate_property", string="Property")
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline")

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            if record.create:
                record.date_deadline = datetime.now() + relativedelta(days=record.validity)
            else:
                record.date_deadline = record.create_date.date() + relativedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

    @api.depends("property_id")
    def action_accept_offer(self):
        for record in self:
            if record.status == "accepted" or record.property_id.state in ['cancelled', 'sold', 'offer_accepted']:
                return False
            record.property_id.selling_price = record.price
            record.property_id.state = 'offer_accepted'
            record.property_id.buyer_id = record.partner_id
            record.status = 'accepted'
        return True

    @api.depends("property_id")
    def action_refuse_offer(self):
        for record in self:
            if record.property_id.state in ['cancelled', 'sold']:
                return False
            record.status = 'refused'
        return True
