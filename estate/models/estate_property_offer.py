from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        [
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True, readonly=True)
    property_type_id = fields.Many2one(
        "estate.property.type",
        related="property_id.property_type_id",
        string="Property Type",
        store=True,
    )
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )
    _check_price = models.Constraint(
        "CHECK(price > 0)",
        "The offer price must be strictly positive.",
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            base_date = (
                offer.create_date.date() if offer.create_date else fields.Date.today()
            )
            offer.date_deadline = fields.Date.add(
                base_date,
                days=offer.validity,
            )

    @api.constrains("date_deadline")
    def _check_date_deadline(self):
        today = fields.Date.today()
        for offer in self:
            if offer.date_deadline < today:
                raise UserError(_("The deadline cannot be earlier than today."))

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.date_deadline:
                base_date = (
                    offer.create_date.date()
                    if offer.create_date
                    else fields.Date.today()
                )
                offer.validity = (offer.date_deadline - base_date).days

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_record = self.env["estate.property"].browse(vals["property_id"])
            if property_record.offer_ids:
                max_offer = max(property_record.offer_ids.mapped("price"))
                if float_compare(vals.get("price", 0), max_offer, precision_rounding=0.01) < 0:
                    raise UserError(_("The offer must be higher than %.2f", max_offer))
            property_record.state = "offer_received"
        return super().create(vals_list)

    def action_accept(self):
        self.status = "accepted"
        other_offer = self.property_id.offer_ids - self
        other_offer.status = "refused"
        self.property_id.selling_price = self.price
        self.property_id.buyer_id = self.partner_id
        self.property_id.state = "offer_accepted"

    def action_refuse(self):
        self.status = "refused"
