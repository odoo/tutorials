from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float(string="Price")
    status = fields.Selection(
        [
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        string="Status",
        copy=False,
    )
    partner_id = fields.Many2one(
        "res.partner",
        string="Partner",
        required=True,
    )
    property_id = fields.Many2one(
        "estate.property", string="Property", required=True, ondelete="cascade"
    )
    property_type_id = fields.Many2one(
        "estate.property.type",
        related="property_id.property_type_id",
        store=True,
        readonly=True,
    )
    validity = fields.Integer(default=7, string="Validity (days)")
    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        string="Deadline",
    )

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date
            if create_date:
                record.date_deadline = create_date.date() + relativedelta(
                    days=record.validity
                )
            else:
                record.date_deadline = fields.Date.today() + relativedelta(
                    days=record.validity
                )

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                record.validity = (
                    record.date_deadline - record.create_date.date()
                ).days

    @api.model
    def create(self, vals_list):
        for vals in vals_list:
            price = vals.get("price", 0.0)
            property_id = vals.get("property_id")
            property_rec = self.env["estate.property"].browse(property_id)
            if not property_rec.exists():
                raise ValidationError(_("Invalid Property."))

            if property_rec.offer_ids:
                max_offer = max(property_rec.offer_ids.mapped("price"))
                if price <= max_offer:
                    raise ValidationError(
                        _("The offer must be higher than existing offers")
                    )

        offers = super().create(vals_list)
        for i in offers:
            i.property_id.state = "offer_received"

        return offers

    def action_accept(self):
        for record in self:
            if record.property_id.offer_ids.filtered(lambda o: o.status == "accepted"):
                raise UserError("Only one offer can be accepted")
            record.status = "accepted"
            record.property_id.write(
                {
                    "buyer_id": record.partner_id,
                    "selling_price": record.price,
                    "state": "offer_accepted",
                }
            )
            return True

    def action_refuse(self):
        self.write({"status": "refused"})
        return True

    _check_price = models.Constraint(
        "CHECK(price > 0)", "The Offer price must be strictly positive"
    )
