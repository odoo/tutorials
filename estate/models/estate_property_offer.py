from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Table for offers of a property"

    price = fields.Float("Price")
    status = fields.Selection(
        string="Status",
        copy=False,
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
    )
    partner_id = fields.Many2one("res.partner", required=True, string="Partner")
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7, string="Validity (days)")
    date_deadline = fields.Datetime(
        compute="_date_deadline", inverse="_set_date_deadline"
    )

    @api.depends("create_date", "validity")
    def _date_deadline(self):
        for record in self:
            record.date_deadline = fields.Datetime.add(
                record.create_date or fields.Datetime.now(), days=record.validity
            )

    def _set_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date).days
