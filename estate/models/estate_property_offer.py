# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EstatePropertyOffer(models.Model):
    _name = 'estate_property_offer'
    _description = 'Real Estate Property Offer'

    price = fields.Float()
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ])

    partner_id = fields.Many2one('res.partner')
    property_id = fields.Many2one('estate_property')
    property_type_id = fields.Char(
        related='property_id.property_type_id',
        store=True
    )

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for rec in self:
            rec.date_deadline = rec.create_date + \
                fields.timedelta(days=rec.validity)

    def _inverse_date_deadline(self):
        for rec in self:
            rec.validity = (rec.date_deadline - rec.create_date).days

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute='_compute_date_deadline',
        inverse='_inverse_date_deadline',
    )
