from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"

    price = fields.Float(string="Price")
    status = fields.Selection(
        [
            ("accepted", "Accepted"),
            ("refused", "Refused")
        ],
        string="Status",
        copy=False
    )
    partner_ids = fields.Many2one(
        "res.partner",
        required=True,
    )
    property_ids = fields.Many2one("estate.property", required=True, ondelete="cascade")
    validity = fields.Integer(default=7, string="Validity (days)")
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True,
    )
    property_type_ids = fields.Many2one(
        comodel_name="estate.property.type",
        string="Property Type",
        related="property_ids.property_type_ids",
        store=True,
    )

    _check_price = models.Constraint(
        'CHECK(price > 0)',
        'Offer Price can be strictly positive'
    )
    _unique_partner_property = models.Constraint(
        "UNIQUE(property_ids, partner_ids)",
        "A partner can only submit one offer per property!"
    )

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for offer in self:
            start_date = (
                offer.create_date.date() if offer.create_date else fields.Date.today()
            )
            offer.date_deadline = fields.Date.add(
                start_date,
                days=offer.validity
            )

    def _inverse_date_deadline(self):
        for offer in self:
            start_date = (
                offer.create_date.date() if offer.create_date else fields.Date.today()
            )

            offer.validity = (offer.date_deadline - start_date).days

    def action_to_accept_offer(self):
        self.ensure_one()
        refused_offer = self.property_ids.offer_ids - self
        refused_offer.status = "refused"
        self.status = "accepted"
        self.property_ids.buyer_ids = self.partner_ids
        self.property_ids.selling_price = self.price
        self.property_ids.state = "offer_accepted"

    def action_to_reject_offer(self):
        self.status = "refused"
        return True

    @api.model
    def create(self, vals_list):
        for vals in vals_list:
            property = self.env["estate.property"].browse(vals["property_ids"])

            if property.offer_ids:
                highest_offer = max(property.offer_ids.mapped("price"))

                if vals["price"] <= highest_offer:
                    raise UserError("The Offer must higher than the existing price")

        offers = super().create(vals_list)
        offers.mapped("property_ids").state = "offer_received"
        return offers
