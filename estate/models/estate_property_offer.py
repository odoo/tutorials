from datetime import timedelta
from dateutil.utils import today

from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Estate Property Offer"
    _order = "price desc"
    _sql_constraints = [
        ('check_price', 'CHECK(price >= 0)', "The offer price must be strictly positive.")
    ]

    price = fields.Float()
    status = fields.Selection(
        copy=False,
        selection=[
            ('accepted', "Accepted"),
            ('refused', "Refused"),
        ]
    )
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)
    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True)

    validity = fields.Integer(default=7, string="Validity (days)")
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse='_inverse_date_deadline', string="Deadline")

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date or today()
            record.date_deadline = create_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            create_date = record.create_date or today()
            record.validity = (record.date_deadline - create_date.date()).days

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            self.env['estate.property'].browse(vals['property_id']).check_new_offer(vals['price'])

        return super().create(vals_list)

    def action_accept(self):
        for record in self:
            self.property_id.accept_offer(record)
        return True

    def action_refuse(self):
        for record in self:
            record.status = 'refused'
        return True
