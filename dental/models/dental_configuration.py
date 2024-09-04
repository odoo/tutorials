from odoo import api, models, fields


class DentalConfiguration(models.Model):

    _name = "dental.configuration"
    _description = "Dental Configuration"

    name = fields.Char(string='Name')
