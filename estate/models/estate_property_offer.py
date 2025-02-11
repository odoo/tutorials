from odoo import models, fields, api
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer's"
    # ch-11 ex-3
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")], copy=False
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(string="Validity (Days)", default=7)
    date_deadline = fields.Date(
        string="Deadline", compute="_compute_deadline", inverse="_inverse_deadline"
    )

    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)',
         'The Offer Price Must be Positive Value')
    ]

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = (
                    record.create_date
                    + fields.date_utils.relativedelta(days=record.validity)
                )
            else:
                record.date_deadline = (
                    fields.Datetime.now()
                    + fields.date_utils.relativedelta(days=record.validity)
                )

    # This method calculate the validity based on change in deadline
    # here type of create_date is datetime while type of date_deadline is date so need type conversion to date
    def _inverse_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = (
                    record.date_deadline - record.create_date.date()
                ).days
            else:
                record.valpassidity = (record.date_deadline -
                                       fields.Datetime.now()).days

    def action_accept_offer(self):
        """Accept an offer and update the property's state"""
        for record in self:
            if record.property_id.selling_price and record.property_id.state == "offer_accepted":
                raise UserError("An offer has already been accepted for this property!")

            if record.status == "accepted":
                raise UserError("This offer has already been accepted!")

            if record.property_id.state == "sold":
                raise UserError("This property has already been sold!")

            record.property_id.state = "offer_accepted"
            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.property_buyer_id = record.partner_id.id
        return True

    def action_refuse_offer(self):
        """Refuse an offer and reset the property state if necessary"""
        for record in self:
            if record.status == "accepted":
                record.property_id.state = "offer_received"
                record.property_id.selling_price = None
                record.property_id.property_buyer_id = None

            record.status = "refused"
        return True