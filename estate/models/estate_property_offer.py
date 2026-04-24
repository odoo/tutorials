from odoo import models, fields, api
from odoo.exceptions import UserError


class Estate_property_offer(models.Model):
    _name = "estate_property_offer"
    _description = "Offer for estate properties"
    _order = "price desc"

    price = fields.Float(required=True)
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate_property", string="Property", required=True)
    state = fields.Selection([
        ('new', 'New'),
        ("accepted", "Accepted"),
        ("refused", "Refused"),
    ], default="new", string="State", copy=False)
    validaty = fields.Integer(string="Offer Validity (days)", default=7)
    date_deadline = fields.Date(string="Offer Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)

    _check_price = models.Constraint(
        "CHECK(price > 0)",
        message="The price must be strictly positive",
    )

    @api.depends("validaty", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            date = record.create_date
            if not date:
                date = fields.Date.today()
            if record.validaty:
                record.date_deadline = fields.Date.add(date, days=record.validaty)
            else:
                record.date_deadline = False

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline and record.create_date:
                create_date = fields.Date.to_date(record.create_date)
                record.validaty = (record.date_deadline - create_date).days
            else:
                record.validaty = 0

    def accept_offer(self):
        for record in self:
            if record.state == "accepted" or record.state == "refused":
                raise UserError("This offer has already been accepted or refused.")
            for offer in record.property_id.offer_ids:
                if offer.state == "accepted":
                    raise UserError("Another offer has already been accepted for this property.")
            record.state = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
        return True

    def refuse_offer(self):
        for record in self:
            if record.state != "new":
                raise UserError("This offer has already been accepted or refused.")
            record.state = "refused"
        return True
