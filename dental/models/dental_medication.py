from odoo import fields, models


class Medication(models.Model):
    _name = "dental.medication"
    _description = "Medication"

    name = fields.Char("Name", required=True)
