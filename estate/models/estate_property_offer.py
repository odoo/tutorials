from odoo import models, fields, api


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer for a real estate property"

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused")
        ],
        copy=False
    )
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline", string="Deadline")

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            tmp_date = fields.Date.today()
            if offer.create_date:
                tmp_date = offer.create_date

            offer.date_deadline = fields.Date.add(tmp_date, days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            start_date = fields.Date.from_string(offer.create_date)
            end_date = fields.Date.from_string(offer.date_deadline)
            difference = (end_date - start_date).days
            offer.validity = difference

    def action_accept(self):
        for record in self:
            record.property_id.offer_ids.mapped(lambda r: r.action_refuse())
            record.status = "accepted"
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price

    def action_refuse(self):
        for record in self:
            record.status = "refused"
