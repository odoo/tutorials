from odoo import models, fields, api
from datetime import timedelta


class PropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'the estate property tag'
    _order = 'name'

    name = fields.Char(required=True)
    color = fields.Integer(string="Color")

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse='_inverse_date_deadline', store=True)

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for offer in self:
            start_date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.date_deadline = start_date + timedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            start_date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.validity = (offer.date_deadline - start_date).days

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Tag name already exists!'),
    ]
