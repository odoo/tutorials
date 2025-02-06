from odoo import api, fields, models
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer list for estate properties"

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + relativedelta(
                    days=record.validity
                )
            else:
                record.date_deadline = fields.Date.today() + relativedelta(
                    days=record.validity
                )

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                record.validity = (record.date_deadline - fields.Date.today()).days
            else:
                record.validity = 7

    def action_confirm(self):
        for record in self:
            if record.status == "accepted":
                raise ValidationError("Already accepted.")
            else:
                record.status = "accepted"
                record.property_id.partner_id = record.partner_id
                record.property_id.selling_price = record.price
                other_offers = self.search(
                    [
                        ("property_id", "=", record.property_id.id),
                        ("id", "!=", record.id),
                        "|",
                        ("status", "=", ""),
                        ("status", "=", "accepted"),
                    ]
                )
            other_offers.write({"status": "refused"})
        return True

    def action_refuse(self):
        for record in self:
            if record.status == "refused":
                raise ValidationError("Already refused.")
            else:
                record.status = "refused"
        return True

    price = fields.Float(string="Price")
    status = fields.Selection(
        string="Status",
        copy=False,
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        help="Status of the offer",
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(string="Validity", default="7")
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )
