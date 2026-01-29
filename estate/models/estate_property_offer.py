from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools import float_compare


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float(string="Price")
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    property_type_id = fields.Many2one(
        related="property_id.property_type_id",
        string="Property Type",
        store=True,
    )
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True,
    )
    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        string="Status",
        copy=False,
    )

    _positive_price = models.Constraint(
        "CHECK (price > 0)",
        "Price must be positive",
    )

    @api.model
    def create(self, vals):
        for record in vals:
            this_property = self.env["estate.property"].browse(record["property_id"])
            if float_compare(this_property.best_offer, record["price"], precision_digits=2) > 0:
                raise UserError("Can't create offer with less price than best price.")
            if this_property.state in ["sold", "canceled", "offer_accepted"]:
                raise UserError("Can't create offer for sold, accepted or canceled property.")
            this_property.state = "offer_received"
        return super().create(vals)

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            base_date = fields.Date.to_date(record.create_date) or fields.Date.today()
            record.date_deadline = fields.Date.add(
                base_date,
                days=record.validity,
            )

    def _inverse_date_deadline(self):
        for record in self:
            base_date = fields.Date.to_date(record.create_date) or fields.Date.today()
            record.validity = (record.date_deadline - base_date).days

    def action_accept(self):
        for record in self:
            if record.property_id.state in ["offer_accepted", "sold", "canceled"]:
                raise UserError("Can't accept offer for sold, accepted or canceled property.")
            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            record.property_id.state = "offer_accepted"

    def action_refuse(self):
        for record in self:
            record.status = "refused"
