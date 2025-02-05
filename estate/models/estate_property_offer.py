from odoo import api, fields, models
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

    price = fields.Float(string="Price")
    status = fields.Selection(
        string="Status",
        copy=False,
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        help="Status of the offer",
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(string="Validity", default="7")
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )
