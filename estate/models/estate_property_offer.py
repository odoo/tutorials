from odoo import models, fields, api


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float(string="Price", required=True)
    validity = fields.Integer(string="Validity", default=7)
    deadline_date = fields.Date(string="Deadline", compute="_compute_deadline_date", inverse="_inverse_deadline_date")
    status = fields.Selection(
        string="Status",
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused")
        ],
        copy=False
    )
    property_id = fields.Many2one("estate.property", string="Property", required=True, ondelete="cascade")
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)

    @api.depends("create_date", "validity")
    def _compute_deadline_date(self):
        for record in self:
            record.deadline_date = fields.Date.add(record.create_date or fields.Date.today(), days=record.validity)

    def _inverse_deadline_date(self):
        for record in self:
            record.validity = (record.deadline_date - fields.Date.today()).days
