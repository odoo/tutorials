from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "estate property offers"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        [
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        string="Status",
        copy=False
    )
    partner_id = fields.Many2one(
        "res.partner",
        required=True
    )
    property_id = fields.Many2one(
        "estate.property",
    )
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline"
    )
    property_type_id = fields.Many2one(
        "estate.property.type",
        related="property_id.property_type_id",
        store=True
    )

    _check_price = models.Constraint(
        'CHECK(price > 0)',
        'An offer price must be strictly positive'
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + \
                    timedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                record.validity = (record.date_deadline -
                                   record.create_date.date()).days

    @api.model
    def create(self, vals_list):
        for vals in vals_list:
            current_price = vals.get('price')
            property = self.env['estate.property'].browse(vals['property_id'])
            for offer in property.offer_ids:
                if current_price < offer.price:
                    raise UserError(
                        "Offer price must greater than minimum price")

        offers = super().create(vals_list)
        for record in offers:
            if record.property_id.state == 'new':
                record.property_id.state = 'offer_received'

        return offers

    def action_confirm(self):
        for record in self:
            for offer in record.property_id.offer_ids:
                if offer.status == "accepted":
                    raise UserError(_("Only one offer can be accepted."))
            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            record.property_id.state = "offer_accepted"

            offers = self.property_id.offer_ids.filtered(lambda x: x.status != "accepted")
            offers.write({'status': 'refused'})

    def action_cancel(self):
        for record in self:
            if record.status == 'accepted':
                record.property_id.selling_price = False
                record.property_id.buyer_id = False
            record.status = "refused"

    def _cron_automatic_refuse(self):
        today = fields.Datetime.now()
        offers = self.search([
            ('status', "not in", ["accepted", "refused"]),
        ])
        for offer in offers:
            expiry_date = offer.create_date + timedelta(days=offer.validity)
            if expiry_date < today:
                offer.write({
                    'status': 'refused'
                })
