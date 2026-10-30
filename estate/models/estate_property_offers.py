from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import UserError


class PropertyOffer(models.Model):
    _name = "estate.property.offers"
    _description = "this model is used to define the offers received to the property"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")], default=False, copy=False
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one(
        "estate.property", required=True, ondelete="cascade")
    property_type_id = fields.Many2one(related="property_id.property_type_id")
    deadline = fields.Date(
        default=lambda _: fields.Date.today() + relativedelta(days=7),
        copy=False,
        compute="_compute_deadline",
        inverse="_inverse_deadline",
        store=True,
    )
    validity_days = fields.Integer(default=7, copy=False)

    _check_price = models.Constraint(
        "check(price>0)", "Offer price must be strictly positive"
    )

    @api.depends("validity_days")
    def _compute_deadline(self):
        for records in self:
            base_date = (
                records.create_date.date()
                if records.create_date
                else fields.Date.today()
            )
            records.deadline = base_date + \
                relativedelta(days=records.validity_days)

    def _inverse_deadline(self):
        for records in self:
            base_date = (
                records.create_date.date()
                if records.create_date
                else fields.Date.today()
            )
            diff = relativedelta(records.deadline, base_date)
            records.validity_days = diff.days

    def action_confirm(self):
        offers = self.property_id.offer_ids.filtered(lambda r: r.id != self.id)
        offers.status = "refused"
        self.status = "accepted"
        self.property_id.buyer = self.partner_id
        self.property_id.state = "offer_accepted"
        self.property_id.selling_price = self.price

    def action_cancel(self):
        for rec in self:
            rec.status = "refused"

    @api.model
    def create(self, vals):
        property_id = None
        for val in vals:
            property_id = val["property_id"]
            price = val["price"]

            last_offer = self.search(
                ["&", ("property_id", "=", property_id),
                 ("status", "!=", "refused")],
                order="id desc",
                limit=1,
            )

            if last_offer and price < last_offer.price:
                raise UserError(
                    "Current Property Offer price cannot be less than the previous Offer"
                )

        if property_id:
            properties = self.env["estate.property"].search(
                [("id", "=", property_id)])
            properties.state = "offer_received"
        return super().create(vals)

    @api.ondelete(at_uninstall=False)
    def _unlink_offer(self):
        if len(self) == len(self.property_id.offer_ids):
            self.property_id.state = "new"
