from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"

    price = fields.Float(required=True)
    is_suspicious = fields.Boolean(
        string="Suspicious",
        compute="_compute_is_suspicious",
    )
    status = fields.Selection(
        selection=[
            ('accepted', "Accepted"),
            ('rejected', "Rejected"),
        ],
        copy=False,
        string="Status",
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(string="Validity", default=7)
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )

    _check_price = models.Constraint(
        "CHECK(price > 0)",
        "A property offer price must be strictly positive",
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                create_date = record.create_date.date()
            else:
                create_date = fields.Date.today()
            record.date_deadline = create_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date:
                create_date = record.create_date.date()
            else:
                create_date = fields.Date.today()
            if record.date_deadline:
                record.validity = (record.date_deadline - create_date).days

    @api.depends("create_date", "partner_id")
    def _compute_is_suspicious(self):
        partner_ids = self.partner_id.ids
        datetimes = [r.create_date for r in self if r.create_date] or [
            fields.Datetime.now(),
        ]
        min_date = min(datetimes) - timedelta(minutes=5)
        max_date = max(datetimes) + timedelta(minutes=5)

        all_partner_offers = self.search(
            [
                ("partner_id", "in", partner_ids),
                ("create_date", ">=", min_date),
                ("create_date", "<=", max_date),
            ],
        )

        for record in self:
            if not record.partner_id or not record.create_date:
                record.is_suspicious = False
                continue

            limit_start = record.create_date - timedelta(minutes=5)
            limit_end = record.create_date + timedelta(minutes=5)
            recent = all_partner_offers.filtered(
                lambda o: (
                    o.partner_id == record.partner_id
                    and limit_start <= o.create_date <= limit_end
                ),
            )
            record.is_suspicious = len(recent) > 2

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("property_id"):
                prop = self.env["estate.property"].browse(vals["property_id"])
                if prop.state in ("offer_accepted", "booked", "sold", "cancelled"):
                    raise UserError(_("You cannot create an offer for a property that is already accepted, booked, sold, or cancelled."))
                for offer in prop.offer_ids:
                    if float_compare(vals.get("price", 0), offer.price, precision_rounding=0.01) < 0:
                        raise UserError(_("You cannot create an offer with a lower amount than an existing offer."))
                prop.state = "offer_received"
        return super().create(vals_list)

    def action_accept(self):

        self.ensure_one()
        if self.status in ("accepted", "rejected"):
            raise UserError(_("This offer has already been accepted, rejected, or cancelled. Please create a new offer."))
        if self.property_id.state in ("offer_accepted", "booked", "sold", "cancelled") or self.property_id.buyer_id:
            raise UserError(_("An offer has already been accepted for this property."))

        self.status = "accepted"
        self.property_id.write({
            'buyer_id': self.partner_id.id,
            'selling_price': self.price,
            'state': 'offer_accepted',
        })
        other_offers = self.property_id.offer_ids - self
        other_offers.write({'status': 'rejected'})

        self.env["estate.property.booking"].create({
            "property_id": self.property_id.id,
            "partner_id": self.partner_id.id,
            "total_amount": self.price,
            "booking_date": fields.Date.context_today(self),
            "state": "draft",
        })
        return True

    def action_refuse(self):
        self.ensure_one()
        if self.status == "accepted":
            raise UserError(_("An accepted offer cannot be refused directly. Please cancel the associated property booking."))
        self.status = "rejected"
        return True
