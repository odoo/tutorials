from odoo import models, fields, api

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"

    price = fields.Float()
    status = fields.Selection(
        string="Status",
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused')],
        copy=False,
    )
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)
    date_deadline = fields.Date(copy=False, default=fields.Date.today(), compute='_compute_date_deadline', inverse='_inverse_date_deadline', store=True)
    validity = fields.Integer(default=7, store=True)

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            reference_date = record.create_date or fields.Datetime.now()
            record.date_deadline = fields.Date.add(fields.Date.from_string(reference_date), days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            reference_date = record.create_date or fields.Datetime.now()
            reference_date = fields.Date.from_string(reference_date)
            if record.date_deadline:
                record.validity = (record.date_deadline - reference_date).days
