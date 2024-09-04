from odoo import api, models, fields


class DentalAllergies(models.Model):

    _name = "dental.allergies"
    _description = "Dental Allergies"

    name = fields.Char(string='Name')
