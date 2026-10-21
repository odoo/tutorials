from odoo import fields, models, api


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer for the properties of the estate module"

    price = fields.Float()
    status = fields.Selection(
        string="Status",
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        help='Current status of the offer (Accepted or Refused).'
    )
    partner_id = fields.Many2one("res.partner", string="Partner")
    property_id = fields.Many2one("estate.property", string="Properties")
    validity = fields.Integer(default=7, compute="_inverse_date_deadline", inverse="_compute_date_deadline")
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            start_date = record.create_date or fields.Date.today()
            record.date_deadline = fields.Date.add(start_date, days=record.validity)

    @api.depends("date_deadline", "validity")
    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - fields.Date.today()).days
