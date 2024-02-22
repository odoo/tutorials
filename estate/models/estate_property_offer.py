from odoo import api, models, fields


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate property offer"

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused")],
        copy=False)

    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_deadline",
        inverse="_inverse_deadline")

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Date().today()
            record.date_deadline = fields.Date.add(
                create_date,
                days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Date().today()
            record.validity = (record.date_deadline -
                               create_date.date()).days
