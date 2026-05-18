from odoo import models, fields

class PrivacyTerms(models.TransientModel):
    _name = 'privacy.terms'
    _description = 'Privacy Policy & Terms of Service'
    # No fields needed – just a placeholder for the view