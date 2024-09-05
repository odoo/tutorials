from odoo import models, fields


class DentalMedicalAids(models.Model):

    _name = "dental.medical.aids"
    _description = "Dental medical aids"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string='Name', required=True)
    partner_id = fields.Many2one(comodel_name="res.partner", string="Contact")
    phone = fields.Char(string='Phone no.', related='partner_id.phone')
    email = fields.Char(related='partner_id.email')
    company_id = fields.Many2one(comodel_name="res.company", string="Company")
    notes = fields.Text()
    image = fields.Image(related='partner_id.image_1920')
