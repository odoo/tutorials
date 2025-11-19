from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float()
    status = fields.Selection(
        string="Status",
        copy=False,
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ]
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    create_date = fields.Date(readonly=True, default=fields.Date.today())
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_reverse_date_deadline")

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(record.create_date if record.create_date is not None else fields.Date.today(), days=record.validity)

    def _reverse_date_deadline(self):
        for record in self:
            record.validity = fields.Date.substract(record.date_deadline, )
