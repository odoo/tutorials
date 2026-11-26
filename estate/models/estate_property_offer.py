from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False,
        readonly=True,
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        string="Deadline",
    )
    property_type_id = fields.Many2one(related="property_id.property_type_id")

    _check_price = models.Constraint(
        "CHECK(price > 0)",
        "The price of an offer must be strictly positive.",
    )

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for offer in self:
            start_date = offer.create_date if offer.create_date else fields.Date.today()
            offer.date_deadline = fields.Date.add(start_date, days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            start_date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.validity = (offer.date_deadline - start_date).days

    @api.model_create_multi
    def create(self, vals_list):
        properties = self.env["estate.property"].browse(vals.get("property_id") for vals in vals_list)  # Prefetching to limit db requests
        properties.mapped("offer_ids.price")
        property_map = properties.grouped("id")

        for vals in vals_list:
            property_record = property_map.get(vals.get("property_id"), self.env["estate.property"])
            if property_record.state in ["sold", "cancelled"]:
                raise UserError(self.env._("Cannot create an offer on a sold/cancelled property"))
            if vals.get("price", 0) <= property_record.best_price:
                raise UserError(self.env._("The offer must be higher than %s !", property_record.best_price))
        return super().create(vals_list)

    def action_accept_offer(self):
        for offer in self:
            if offer.property_id.state == "accepted":
                raise UserError(self.env._("Cannot accept multiple offers."))
            if offer.property_id.state in ["sold", "cancelled"]:
                raise UserError(self.env._("Cannot accept an offer on a sold/cancelled property."))
            offer.status = "accepted"
            (offer.property_id.offer_ids - offer).status = "refused"

    def action_reject_offer(self):
        for offer in self:
            offer.status = "refused"
