from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools.date_utils import add
from odoo.tools.float_utils import float_compare


class EstatePropertayOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"
    _check_price = models.Constraint(
        "CHECK(price>0)",
        "The offer price must be strictly positive",
    )

    price = fields.Float("Price")
    status = fields.Selection(
        string="Status",
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one(
        "estate.property",
        string="Estate Property",
        required=True,
    )
    validity = fields.Integer("Validity (days)", default=7)
    date_deadline = fields.Date(
        "Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )
    property_type_id = fields.Many2one(related="property_id.property_type_id")

    def _get_creation_date(self):
        return self.create_date.date() if self.create_date else fields.Date.today()

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = add(
                record._get_creation_date(),
                days=record.validity,
            )

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - self._get_creation_date()).days

    def action_accept_offer(self):
        for offer in self.property_id.offer_ids:
            offer.status = "refused"
        self.status = "accepted"
        self.property_id.selling_price = self.price
        self.property_id.buyer_id = self.partner_id
        # todo but what if it is updated manually

    def action_refuse_offer(self):
        self.status = "refused"

    @api.constrains("status")
    def _check_offer_accept(self):
        for record in self:
            if record.status != "accepted":
                return
            if (
                float_compare(
                    record.price,
                    0.9 * record.property_id.expected_price,
                    precision_digits=1,
                )
                == -1
            ):
                raise ValidationError(
                    "The selling price must be at least 90% of the expected price! You must reduce the expected price if you want to accept this offer."
                )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property = self.env["estate.property"].browse(vals["property_id"])
            if property.state == "new":
                property.state = "offer_received"

        return super().create(vals_list)
