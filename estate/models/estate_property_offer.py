from dateutil.relativedelta import relativedelta

from odoo import models, fields, api


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "These are Estate Module Property Offer"

    price = fields.Float(string="price")
    state = fields.Selection(
        string="Status", 
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        copy=False
    )
    estate_property_id = fields.Many2one(comodel_name="estate.property", string="Property", required=True)
    partner_id = fields.Many2one(comodel_name="res.partner", string="Partner", required=True)
    validity = fields.Integer(string="Validity (days)", default=7, compute="_compute_validity", inverse="_inverse_validity", store=True)
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True)


    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        print("date_compute")
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.date_deadline = date + relativedelta(days=offer.validity)


    def _inverse_date_deadline(self):
        print("date_inverse")
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.validity = (offer.date_deadline - date).days

    @api.depends("create_date", "date_deadline")
    def _compute_validity(self):
        print("validity_compute")
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.validity = (offer.date_deadline - date).days if offer.date_deadline else 7

    def _inverse_validity(self):
        print("validity_inverse")
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.date_deadline = date + relativedelta(days=offer.validity)
