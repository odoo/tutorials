# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, exceptions, _
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offers of Estate property "
    _order = "price desc"

    price = fields.Float(string="Price")
    status = fields.Selection(
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        copy=False,
        string="Status",
    )
    validity = fields.Integer(string="Validity", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_deadline_date", inverse="_inverse_deadline_date")
    partner_id = fields.Many2one("res.partner", string="Partner", copy=False, required=True, store=True)
    property_id = fields.Many2one("estate.property", copy=False, required=True)
    property_type_id = fields.Many2one(
        "estate.property.type",
        related="property_id.property_type_id",
        store=True,
        readonly=False,
    )

    _sql_constraints = [(
        "check_offer_price",
        "CHECK(price > 0)",
        "The Offer price must be strictly positive",
    )]

    @api.depends("create_date", "validity")
    def _compute_deadline_date(self):
        for offer in self:
            create_dt = offer.create_date or fields.Date.today()
            offer.date_deadline = create_dt + relativedelta(days=offer.validity)

    def _inverse_deadline_date(self):
        for offer in self:
            if offer.date_deadline:
                create_dt = (offer.create_date or fields.Datetime.now()).date()
                delta = (offer.date_deadline - create_dt).days
                offer.validity = delta
            else:
                offer.validity = 0

    def action_accept(self):
        for offer in self:
            if offer.property_id.buyer_id:
                raise UserError(_("An offer has already been accepted for this property."))
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.selling_price = offer.price
            offer.status = "accepted"
            offer.property_id.state = "offer_accepted"
            other_offers = offer.property_id.offer_id - offer
            other_offers.write({"status": "refused"})
        return True

    def action_refused(self):
        for offer in self:
            offer.status = "refused"
        return True

    @api.model_create_multi
    def create(self, vals_list):
        new_records = []
        for vals in vals_list:
            property_id = vals.get("property_id")
            property_rec = self.env["estate.property"].browse(property_id)
            if property_rec.state == "sold":
                raise exceptions.ValidationError(_("You cannot create an offer for a property that is already sold."))
            if property_rec.state == "new":
                property_rec.state = "offer_received"
            if "price" in vals and vals["price"] < property_rec.best_price:
                raise exceptions.ValidationError(
                    "Offer price must be higher than existing offers."
                )
            new_records.append(vals)
        return super().create(new_records)
