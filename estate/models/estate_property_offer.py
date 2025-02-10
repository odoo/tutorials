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
        for record in self:
            if record.property_id.state == "offer accepted":
                raise UserError("An offer Already Accepted for this Property")

        if self.status == "accepted":
            raise UserError(
                (f"You can't Accept an offer it's already {self.status}"))
        elif self.property_id.state == "sold":
            raise UserError("Property Already Sold")

        self.property_id.state = "offer accepted"
        self.status = "accepted"
        self.property_id.selling_price = self.price
        self.property_id.property_buyer_id = self.partner_id.id
        return True

    def action_refuse_offer(self):
        if self.status == "refused":
            raise UserError(
                (f"You can't Refuse an offer it's already {self.status.capitalize()}"))
        elif self.status == "accepted":
            self.property_id.state = "offer received"
            self.property_id.selling_price = None
            self.property_id.property_buyer_id = None

        self.status = "refused"
        return True