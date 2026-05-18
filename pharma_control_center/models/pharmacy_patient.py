from odoo import fields, models


class PharmacyPatient(models.Model):
    _name = "pharmacy.patient"
    _description = "Patient"
    _order = "name"

    doctor_id = fields.Many2one('res.users', string="Assigned Doctor", required=True)
    name = fields.Char(string="Patient Name", required=True)
    age = fields.Integer(string="Age")
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], string="Gender")
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")
    address = fields.Text(string="Address")
    blood_group = fields.Selection([
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
    ], string="Blood Group")
    medical_history = fields.Text(string="Medical History")
    allergies = fields.Text(string="Allergies")
    # Removed prescription_ids - will be added later with a proper prescription model
    active = fields.Boolean(string="Active", default=True)

    _sql_constraints = [
        ('unique_email', 'UNIQUE(email)', 'Email must be unique!'),
    ]
