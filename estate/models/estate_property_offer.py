from datetime import timedelta
from odoo import models, fields,api

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    price = fields.Float(string='Price')
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ], string='Status', default='refused', required=True)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)

    validity = fields.Integer(string="Validity (Days)", default=7)
    date_deadline = fields.Date(
        string="Deadline", 
        compute="_compute_date_deadline", 
        inverse="_inverse_date_deadline", 
        store=True
    )



    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        """Compute the date_deadline based on create_date and validity."""
        for offer in self:
            if offer.create_date:  # Ensure create_date is not None
                offer.date_deadline = offer.create_date + timedelta(days=offer.validity)
            else:
                offer.date_deadline = fields.Date.today() + timedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        """Set the validity field based on date_deadline."""
        for offer in self:
            if offer.create_date and offer.date_deadline:
                delta = (offer.date_deadline - offer.create_date.date()).days
                offer.validity = delta