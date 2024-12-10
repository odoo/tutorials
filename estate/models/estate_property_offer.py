from odoo import api,models, fields
class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float(required=True)
    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        string="Status",
        default="None",
    )
    partner_id = fields.Many2one(
        'res.partner',
        string="Partner",
        required=True,
    )
    property_id = fields.Many2one(
        'estate.property',
        string="Property",
        required=True,
    )
    validity=fields.Integer(
        string="Validity (days)",
        default=7,
    )
    date_deadline=fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )
    @api.depends("create_date","validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = fields.Date.add(record.create_date, days=record.validity)
            else:
                record.date_deadline = fields.Date.add(fields.Date.today(),days=record.validity)
    def _inverse_date_deadline(self):
        for record in self:
                record.validity = fields.Date.subtract(record.date_deadline - fields.Date.to_date(record.create_date)).days


                