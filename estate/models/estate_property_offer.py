from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer for properties"

    price = fields.Float(string="Price")
    status = fields.Selection(
        string="Status",
        selection=[
            ('accepted',"Accepted"),
            ('refused',"Refused"),
        ],
        copy=False
    )
    partner_id = fields.Many2one('res.partner', string="Buyer", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True, ondelete='cascade')
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = fields.Date.add(record.create_date.date(), days=record.validity)
            else:
                record.date_deadline = fields.Date.add(fields.Date.today(), days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                delta = record.date_deadline - record.create_date.date()
                record.validity = delta.days
