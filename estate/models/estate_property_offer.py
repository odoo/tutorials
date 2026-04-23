from odoo import models, fields, api


class Estate_property_offer(models.Model):
    _name = "estate_property_offer"
    _description = "Offer for estate properties"

    price = fields.Float(required=True)
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate_property", string="Property", required=True)
    state = fields.Selection([
        ("accepted", "Accepted"),
        ("refused", "Refused"),
    ], string="State", copy=False)
    validaty = fields.Integer(string="Offer Validity (days)", default=7)
    date_deadline = fields.Date(string="Offer Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    @api.depends("validaty", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            if record.validaty and record.create_date:

                record.date_deadline = fields.Date.add(record.create_date, days=record.validaty)
            else:
                record.date_deadline = False

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline and record.create_date:
                create_date = fields.Date.to_date(record.create_date)
                record.validaty = (record.date_deadline - create_date).days
            else:
                record.validaty = 0
