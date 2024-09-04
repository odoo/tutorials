from odoo import  fields, models


class MedicalAidsModel(models.Model):
    _name = "medical.aids"
    _description = "Medical Aids"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Name") 
    contact = fields.Char(string="Contact") 
    phone_number = fields.Char(string="Phone Number")  
    email = fields.Char(string="Email")
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.company,
    )
    notes = fields.Text()
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("in progress", "In Progress"),
            ("done", "Done"),
        ],
        tracking=True,
        default="new",
    )
    
    