from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.profiler import Profiler


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"

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

    @api.onchange("date_deadline")
    def _onchange_date_deadline(self):
        self._inverse_date_deadline()

    @api.depends("create_date", "partner_id")
    def _compute_is_suspicious(self):
        partner_ids = self.partner_id.ids
        datetimes = [r.create_date for r in self if r.create_date] or [
            fields.Datetime.now()
        ]
        min_date = min(datetimes) - timedelta(minutes=5)
        max_date = max(datetimes) + timedelta(minutes=5)

        all_partner_offers = self.search(
            [
                ("partner_id", "in", partner_ids),
                ("create_date", ">=", min_date),
                ("create_date", "<=", max_date),
            ]
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

    def action_accept(self):
        test_offer = self.env['estate.property.offer'].search([('status', '=', 'non_existent_status')], limit=1)
        breakpoint()
        with Profiler(
            db=None,
            log=True,
            description="testing"
        ):
            self.ensure_one()
            if self.property_id.state in ("sold", "cancelled"):
                raise UserError("You cannot accept an offer for a sold or cancelled property.")
            if self.property_id.buyer_id:
                raise UserError("An offer has already been accepted for this property.")
            self.status = "accepted"
            self.property_id.write({
                'buyer_id': self.partner_id.id,
                'selling_price': self.price,
                'state': 'offer_accepted',
            })
            other_offers = self.property_id.offer_ids - self
            other_offers.status = 'rejected'
            return True

    def action_refuse(self):
        self.ensure_one()
        self.status = "rejected"
        return True

