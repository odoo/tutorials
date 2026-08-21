from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float(string="Offer Price", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )
    status = fields.Selection(
        string="Status",
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False,
    )
    partner_id = fields.Many2one(
        string="Buyer",
        comodel_name="res.partner",
        required=True,
    )
    property_id = fields.Many2one(
        string="Property",
        comodel_name="estate.property",
        required=True,
    )
    property_type_id = fields.Many2one(
        string="Property Type",
        related="property_id.property_type_id",
        store=True,
    )

    _check_positive_price = models.Constraint(
        'CHECK(price > 0)',
        'Offer prices must be a positive amount.',
    )

    # Methods
    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.today() + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - fields.Date.today()).days

    @api.model
    def create(self, vals_list):
        for vals in vals_list:
            property = self.env["estate.property"].browse(vals.get("property_id"))

            if property and property.state in ("sold", "offer_accepted"):
                raise ValidationError(_("Can't create an offer for properties that are sold or with an accepted offer"))

            property.state = "offer_received"

        return super().create(vals_list)

    def action_accept(self):
        for record in self:
            record.status = "accepted"
            record.property_id.state = "offer_accepted"
            record.property_id.partner_id = record.partner_id
            record.property_id.selling_price = record.price

            # Refuse other offers for the same property
            other_offers = self.search([
                ("property_id", "=", record.property_id.id),
                ("id", "!=", record.id),
            ])
            other_offers.write({"status": "refused"})

    def action_refuse(self):
        for record in self:
            record.status = "refused"
