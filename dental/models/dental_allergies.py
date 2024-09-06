from odoo import models, fields


class DentalAllergies(models.Model):
    _name = "dental.allergies"
    _description = "Dental Allergies list "
    _order = "name"

    name = fields.Char(string="Allergies", required=True)
    sequence = fields.Integer(string="Sequence", default=10)
