from odoo import api, models, fields


class EstatePropertyOffer(models.Model):
    _name = "estate_property.offer"
    _description = "Offer to the Estate"

    name = fields.Char('Nom', required=True)
    price = fields.Float('Price')
    status = fields.Selection(
        string="Status",
        selection=[
            ('accepted', "Accepted"),
            ('refused', "Refused"),
        ]
    )
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate_property', string="Property", required=True)

    validity = fields.Integer('Validity')
    date_deadline = fields.Date(compute="_compute_deadline")

    @api.depends("create_date", "validity")
    def _compute_deadline(self):
        for record in self:
            base_date = record.create_date if record.create_date else fields.Date.today()
            record.date_deadline = fields.Date.add(base_date, days=record.validity)
