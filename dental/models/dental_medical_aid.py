from odoo import models, fields


class DentalMedication(models.Model):
    _name = "dental.medical.aid"
    _description = "Medications"
    _order = "name"

    name = fields.Char(string="Medical Aid Name", required=True)
    contact_name = fields.Char(string="Contact")
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")
    company = fields.Many2one("res.company", string="Company")
    notes = fields.Text()
