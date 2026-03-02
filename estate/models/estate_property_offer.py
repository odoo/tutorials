from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offers"
    _order = "price desc"

    price = fields.Float(string="Offer Price", required=True)
    status = fields.Selection(
        [("accepted", "Accepted"), ("rejected", "Rejected")], copy=False
    )
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(string="Validity (day)", default=7)
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )
    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Property Type",
        store=True,
        related="property_id.property_type_id",
    )

    _check_price_positive = models.Constraint(
        "CHECK(price > 0)", "The property offer should be strictly positive"
    )

    def _get_create_date(self):
        return self.create_date.date() if self.create_date else fields.Date.today()

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            date = record._get_create_date()
            record.date_deadline = date + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            date = record._get_create_date()
            record.validity = (record.date_deadline - date).days

    @api.constrains("price")
    def _check_offer_price(self):
        for record in self:
            min_price = record.property_id.expected_price * 0.9
            if float_compare(record.price, min_price, precision_digits=2) == -1:
                raise ValidationError(
                    _("The offer price can not be less than 90% of expected price")
                )

    @api.model
    def create(self, vals_list):
        for vals in vals_list:
            property_rec = self.env["estate.property"].browse(vals["property_id"])
            price = vals.get("price", 0)
            if float_compare(price, property_rec.best_price, precision_digits=2) < 0:
                raise UserError(
                    _("The offer price can not be less than best offer price")
                )
        offers = super().create(vals_list)
        offers.filtered(
            lambda offer: offer.property_id.state == "new"
        ).property_id.write({"state": "offer_received"})
        return offers

    def action_accept(self):
        self.ensure_one()
        if self.property_id.offer_ids.filtered(
            lambda offer: offer.status == "accepted"
        ):
            raise UserError(_("An offer has already been accepted for this property"))
        self.status = "accepted"
        refuse = self.property_id.offer_ids.filtered(lambda offer: not offer.status)
        refuse.write({"status": "rejected"})
        self.property_id.state = "offer_accepted"
        self.property_id.buyer_id = self.partner_id
        self.property_id.selling_price = self.price
        return True

    def action_refuse(self):
        self.ensure_one()
        self.status = "rejected"
        return True
