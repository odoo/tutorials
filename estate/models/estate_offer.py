from odoo import models, fields, api


class EstateProperty(models.Model):
    _name = "estate.property.offer"
    _description = "Estate property offers"

    price = fields.Float(required=True)
    status = fields.Selection(
        selection=[
            ('refused','Refused'), 
            ('accepted','Accepted')
        ],
        copy=False
    )
    validity = fields.Integer(default=7)
    create_date = fields.Date(default=lambda self: fields.Date.today(), readonly=True)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_validity")
    # relations
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)


    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(record.create_date, days=record.validity)


    @api.depends("date_deadline")
    def _inverse_validity(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date).days  