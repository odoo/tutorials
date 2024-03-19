from odoo import fields, models, api

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float(string="Price")
    status = fields.Selection([
        ("accepted", "Accepted"),
        ("refused", "Refused"),
    ], copy=False, string="Status")

    partner_id = fields.Many2one(string="Buyer", comodel_name="res.partner", required=True)
    property_id = fields.Many2one(string="Property", comodel_name="estate.property", required=True)
    validity = fields.Integer(string="Offer Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_deadline_date", inverse="_inverse_deadline_date")

    @api.depends("validity", "create_date")
    def _compute_deadline_date(self):
        for record in self:
            initial_date = record.create_date if record.create_date else fields.Date.today()
            record.date_deadline = fields.Date.add(initial_date, days=record.validity)

    def _inverse_deadline_date(self):
        for record in self:
            initial_date = record.create_date if record.create_date else fields.Date.today()
            record.validity = (record.date_deadline - initial_date).days
