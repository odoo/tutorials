from odoo import fields, models


class Allergies(models.Model):
    _name = "dental.allergies"
    _description = "Allergies Records"
    name = fields.Char(string="Condition Name", required=True)
    description = fields.Text(string="Description")
 