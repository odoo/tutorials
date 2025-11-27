from dateutil.relativedelta import relativedelta

from odoo import fields, models, api
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"
    price = fields.Float()
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        string="Deadline Date",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True
    )
    property_type_id = fields.Many2one(
        related="property_id.property_type_id",
        store=True
    )

    _check_offer_price = models.Constraint(
        'CHECK(price > 0)',
        'The price of an offer must be strictly positive.'
    )

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            creation_date = record.create_date or fields.Date.today()
            record.date_deadline = creation_date + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            creation_date = record.create_date.date() or fields.Date.today()
            record.validity = (record.date_deadline - creation_date).days

    def action_accept(self):
        for record in self:
            if record.property_id.buyer_id:
                raise UserError("Property already has an accepted offer.")
            record.status = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.state = 'offer_accepted'
            record.property_id.buyer_id = record.partner_id

    def action_refuse(self):
        self.status = 'refused'
        return True

    @api.model
    def create(self, vals):
        vals_list = vals if isinstance(vals, list) else [vals]
        property_offer_map = {}
        for v in vals_list:
            pid = v.get("property_id")
            if pid:
                property_offer_map.setdefault(pid, []).append(v)
        for pid, offers in property_offer_map.items():
            prices = [o.get("price") for o in offers if o.get("price") is not None]
            if prices:
                max_new_price = max(prices)
                existing_offers = self.search([
                    ("property_id", "=", pid),
                    ("price", ">=", max_new_price),
                ], limit=1)
                if existing_offers:
                    raise UserError("You cannot create an offer with a lower amount than an existing offer for this property.")

        records = super().create(vals)
        if isinstance(records, models.Model):
            for offer in records:
                offer.property_id.state = "offer_received"
        return records

    @api.model
    def _auto_refuse_pass_deadline_entry(self):
        current_date = fields.Date.today() + relativedelta(days=7)
        invalid_offers = self.search([
            ('date_deadline', '<=', current_date),
            ('status', 'not in', ['accepted', 'refused']),
        ])
        for record in invalid_offers:
            record.status = 'refused'
