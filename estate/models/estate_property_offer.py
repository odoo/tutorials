from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, exceptions


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offers"

    price = fields.Float(string="Price", required=True)
    status = fields.Selection(
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        string="Status",
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", string="Partner")
    property_id = fields.Many2one("estate.property", string="Property")
    validate = fields.Integer(string="Validity(days)", default=7)
    date_deadline = fields.Date(
        string="Deadline",
        default=fields.Date.today(),
        compute="_compute_deadline",
        inverse="_update_validity",
    )

    @api.depends("validate", "create_date")
    def _compute_deadline(self):
        for date in self:
            if date.create_date:
                date.date_deadline = date.create_date + relativedelta(
                    days=date.validate
                )
            else:
                date.date_deadline = fields.Date.today() + relativedelta(
                    days=date.validate
                )

    def _update_validity(self):
        for days in self:
            if days.date_deadline:
                days.validate = (days.date_deadline - fields.Date.today()).days
            else:
                days.validate = 7

    # Function to perform action when offer accpeted
    def action_accept(self):
        for record in self:
            if record.property_id.selling_price and (
                record.status == "accepted" or record.status == "refused"
            ):
                raise exceptions.UserError("This property has already accepted offer!")

            record.property_id.selling_price = record.price
            record.property_id.partner_id = record.partner_id

            record.status = "accepted"

            other_offers = self.search(
                [
                    ("property_id", "=", record.property_id.id),
                    ("id", "!=", record.id),
                    ("status", "=", "refused"),
                ]
            )

            other_offers.write({"status": "refused"})

    # Function to perform action when offer refused
    def action_refuse(self):
        for record in self:
            record.status = "refused"

    # SQL Constraints
    _sql_constraints = [
        (
            "price_positive",
            "CHECK(price > 0)",
            "Offer Price must be strictly positive!",
        ),
    ]


    



