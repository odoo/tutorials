# licence

from odoo import api
from odoo import fields
from odoo import models


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Property offers"

    name = fields.Char("Name", required=False, default="- no name -")
    price = fields.Float("Offer price", required=True)
    validity = fields.Integer("Validity time", default=7)
    # Reserved
    state = fields.Selection(
        string="Status",
        selection=[
            ('accepted', "Accepted"),
            ('refused', "Refused")
            ],
        default=None,
        )
    # Relational
    property_id = fields.Many2one('estate.property', string="Property", required=True)
    partner_id = fields.Many2one('res.partner', string="Buyer", required=True)
    # Computed
    date_deadline = fields.Date("Deadline date", compute='_compute_deadline', inverse='_inverse_deadline')
    # Constrains
    _sql_constraints = [
        ('check_price_positive', 'CHECK(price >= 0)',
         'The offer price must be strictly positive.'),
    ]

    @api.depends('validity', 'create_date')
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add((record.create_date or fields.Date.today()), days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            start_date = (record.create_date and record.create_date.date()) or fields.Date.today()
            record.validity = (record.date_deadline - start_date).days

    def action_accept(self):
        for record in self:
            record.state = 'accepted'
            record.property_id.state = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
        return True

    def action_refuse(self):
        for record in self:
            record.state = 'refused'
        return True
