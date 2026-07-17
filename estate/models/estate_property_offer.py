import datetime

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.tools import SQL


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "this model is for estate property offers"
    # _order = "price desc"

    _check_price = models.Constraint(
        "CHECK(price>0)",
        "Price of offer must be positive.",
    )

    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )
    partner_id = fields.Many2one("res.partner", required=True)
    price = fields.Float()
    property_id = fields.Many2one("estate.property", required=True, ondelete="cascade")
    property_type_id = fields.Many2one(
        'estate.property.type',
        related="property_id.property_type",
        string="Property Type",
    )
    status = fields.Selection(
        [('accepted', "Accepted"), ('refused', "Refused")],
        copy=False,
    )

    validity = fields.Integer(default=7)

    security_status = fields.Selection(
        [('suspicious', 'Suspicious')],
        compute='_compute_security_status',
    )

    @api.depends('partner_id', 'create_date')
    def _compute_security_status(self):
        for offer in self:
            offer.security_status = False

            if not (offer.partner_id and offer.property_id and offer.create_date):
                continue

            offers_count = self.search_count(
                [
                    ('property_id', '=', offer.property_id.id),
                    ('partner_id', '=', offer.partner_id.id),
                    (
                        'create_date',
                        '>=',
                        offer.create_date - datetime.timedelta(seconds=300),
                    ),
                    (
                        'create_date',
                        '<=',
                        offer.create_date + datetime.timedelta(seconds=300),
                    ),
                ],
            )

            if offers_count > 2:
                offer.security_status = 'suspicious'

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for offer in self:
            create_date = offer.create_date or fields.Date.today()
            offer.date_deadline = create_date + relativedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            create_date = offer.create_date.date() or fields.Date.today()
            if offer.date_deadline and create_date:
                offer.validity = (offer.date_deadline - create_date).days

    def action_accept(self):
        for offer in self:
            property_record = offer.property_id

            already_accepted = property_record.offer_ids.filtered(
                lambda o: (
                    o.price == property_record.selling_price and o.status == 'accepted'
                ),
            )

            if already_accepted:
                already_accepted.status = "refused"

            offer.status = "accepted"
            offer.property_id.write(
                {
                    "selling_price": offer.price,
                    "buyer": offer.partner_id.id,
                    "state": "offer_accepted",
                },
            )
            refuse_ids = property_record.offer_ids.filtered(lambda o: not o.status)
            refuse_ids.write({"status": "refused"})
        return True

    def action_make_validity_default(self):
        for offer in self:
            offer.validity = 7
        return True

    def action_refuse(self):
        for offer in self:
            offer.status = "refused"
        return True
