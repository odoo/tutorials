from odoo import models, fields


class ResUsers(models.Model):
    """
    Extends the default res.users model to include additional fields:
    - Address Details
    - Phone Number
    - VAT Number
    """
    _inherit = "res.users"

    address_details = fields.Text(string="Address")  # Stores user's full address details
    phone_number = fields.Char(string="Phone Number")  # Stores user's phone number
    vat_number = fields.Char(string="VAT Number")  # Stores user's VAT identification number
