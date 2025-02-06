from odoo import fields, models


class EstateSalesperson(models.Model):

    _name='estate.salesperson'
    _description="Estate Salesperson"
    _rec_name="salesperson_name"

    salesperson_name=fields.Char(string="Name", required=True)
    salesperson_phone=fields.Integer(string="Phone number", required=True)
    salesperson_email=fields.Char(string="Email", required=True)
    sold_properties=fields.One2many(comodel_name="estate.property", inverse_name="salseperson_id", string="Properties")
    