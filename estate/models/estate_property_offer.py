from odoo import fields, models, api
from datetime import timedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    # Offer details
    price = fields.Float('Price')

    # Status of the offer
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], string='Status')

    # Relations with partner and property
    partner_id = fields.Many2one('res.partner', string='Partner')
    property_id = fields.Many2one('estate.property', string='Property')

    # Validity of the offer in days (default is 7)
    validity = fields.Integer('Validity', default=7)

    # Computed field for offer deadline with inverse function
    date_deadline = fields.Date(
        string="Date Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True
    )

    @api.depends('property_id.create_date', 'validity')
    def _compute_date_deadline(self):
        """
        Compute the deadline date based on property creation date and validity period.
        """
        for record in self:
            if record.property_id and record.property_id.create_date:
                record.date_deadline = record.property_id.create_date.date() + timedelta(days=record.validity)
            else:
                record.date_deadline = False  # Prevents crashes if create_date is missing

    def _inverse_date_deadline(self):
        """
        Allow the user to set either the date_deadline or validity manually.
        """
        for record in self:
            if record.property_id and record.date_deadline:
                record.validity = (record.date_deadline - record.property_id.create_date.date()).days
