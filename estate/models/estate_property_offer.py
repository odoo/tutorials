from odoo import api, models, fields
from dateutil.relativedelta import relativedelta
from datetime import date
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = "estate.property.offer"
    _description = "EstatePropertyOffer"
    _order = "price desc"
    # created the fields for the estate.property.offer model
    name = fields.Char()
    price = fields.Float()
    status = fields.Selection([("accepted", "Accepted"), ("refused", "Refused")])
    partner_id = fields.Many2one("res.partner")
    property_id = fields.Many2one("estate.property")
    Validity = fields.Integer(default=7)
    deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline")
    property_type_id = fields.Many2one(
        related="property_id.property_type_id", store=True
    )

    # created the sql constraints for only accepting positive value to price
    _sql_constraints = [
        (
            "check_price",
            "CHECK(price > 0.0)",
            "An offer price must be strictly positive and Grater then Zero.",
        )
    ]

    # created the compute function to compute deadline as create date + validity
    @api.depends("Validity")
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                pass
            else:
                record.create_date = date.today()
            record.deadline = record.create_date + relativedelta(days=record.Validity)

    @api.onchange("name")
    def _onchange_offer(self):
        if self.name:
            self.property_id.state = "offer_recieved"

    # created the inverse function that will compute the validity when we manually update the deadline i.e deadline - creation date
    def _inverse_deadline(self):
        for record in self:
            record.Validity = (
                record.deadline.toordinal() - record.create_date.toordinal()
            )

    # created the action for the accept button that will accept the offer from the offers for a property.
    def action_accept(self):
        # checks weather any other offer is alredy accepted. if offer is alredy accepted then it will raise an error
        if self.property_id.buyer_id:
            raise UserError("One of the Offer is alredy selected for this property.")
        for record in self:
            record.status = "accepted"
            record.property_id.buyer_id = record.partner_id.id
            record.property_id.selling_price = record.price
            record.property_id.state = "offer_accepted"
        return True

    # created the action for the refuse button that will refuse the offer from the offers for a property
    def action_refuse(self):
        for record in self:
            record.status = "refused"
            record.property_id.buyer_id = ""
