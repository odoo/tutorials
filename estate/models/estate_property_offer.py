from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"

    price = fields.Float(required=True)
    state = fields.Selection(selection=[('accepted', 'Accepted'), ('refused', 'Refused'), ('waiting', 'Waiting for approval')], default='waiting')
    partner_id = fields.Many2one("res.partner", string="Partner")
    property_id = fields.Many2one("estate.property", string="Property")
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    validity = fields.Integer(default=7)

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(fields.Date.today(), days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            create_date = fields.Date.to_date(record.create_date)
            record.validity = (record.date_deadline - create_date).days
