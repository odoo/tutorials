from odoo import fields, models


class EstateCustomer(models.Model):

    _name='estate.customer'
    _description="Estate Customer"
    _rec_name="customer_name"

    customer_name=fields.Char(string= "Name",required=True)
    customer_phone=fields.Integer(string= "Phone Number", required=True)
    customer_email=fields.Char(string= "Email",required=True)
    properties=fields.One2many(comodel_name="estate.property", inverse_name="partner_id", string="Properties")
