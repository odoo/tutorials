from odoo import fields, models


class Customer(models.Model):
    _name = "customer"
    _description = "Customer"

    name = fields.Char(string="Customer Name", required=True)
    phone = fields.Char(string="Phone Number")
    email = fields.Char(string="Email Address")
    address = fields.Char(string="Address")
