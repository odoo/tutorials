from odoo import api, fields, models


class MyModel(models.Model):
    _name = "add.employee"
    _description = "Company Management"
    _order = "id desc"

    name = fields.Char(string="Title", required=True)
    email = fields.Char(string="Email", required=True)
    address = fields.Char(string="Address", required=True)
    department = fields.Char(string="Department", required=True)
