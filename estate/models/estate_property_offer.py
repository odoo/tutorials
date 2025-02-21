from odoo import api, models, fields, exceptions


class Offer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _sql_constraints = [
        (
            "positive_price",
            "CHECK(price > 0)",
            "The price of an offer must be strictly positive",
        ),
    ]
    _order = "price desc"

    price = fields.Float(required=True)
    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    property_type_id = fields.Many2one(
        related="property_id.property_type_id", store=True
    )
    validity = fields.Integer(string="Validity (days)")
    date_deadline = fields.Date(
        compute="_compute_date_deadline", inverse="_inverse_date_deadline"
    )

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(
                record.create_date or fields.Date.today(), days=record.validity
            )

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (
                record.date_deadline - fields.Date.to_date(record.create_date)
            ).days

    @api.model
    def create(self, vals):
        property_ = self.env["estate.property"].browse(vals["property_id"])
        best_price = max(property_.offer_ids.mapped("price"), default=0.0)
        if vals["price"] < best_price:
            raise exceptions.UserError("The offer must be higher than %s" % best_price)
        if property_.state == "new":
            property_.state = "received"
        return super().create(vals)

    def action_accept(self):
        for record in self:
            if record.status == "refused":
                raise exceptions.UserError("Refused offers cannot be accepted")
            if record.property_id.state not in ["new", "received"]:
                raise exceptions.UserError(
                    "Only properties that are new or have only received offers can have an offer accepted"
                )
            record.status = "accepted"
            record.property_id.state = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
        return True

    def action_refuse(self):
        for record in self:
            if record.status == "accepted":
                raise exceptions.UserError("Accepted offers cannot be refused")
            record.status = "refused"
        return True
