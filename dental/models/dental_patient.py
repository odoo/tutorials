from odoo import models, fields, Command, api
from datetime import date


class DentalPatient(models.Model):
    _name = 'dental.patient'
    _description = 'Dental Patient Info'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True)
    state = fields.Selection([
        ('new', 'New'),
        ('to_do_today', 'To do today'),
        ('done', 'Done'),
        ('to_invoice', 'To invoice'),
    ],default="new", tracking = True)
    guarantor_id = fields.Many2one('res.partner', string='Guarantor')
    guarantor_phone = fields.Char(
        string='Guarantor Phone', 
        related='guarantor_id.phone', 
        readonly=True
    )
    guarantor_email = fields.Char(
        string='Guarantor Email', 
        related='guarantor_id.email', 
        readonly=True
    )
    guarantor_company = fields.Char(string="Company", related='guarantor_id.parent_id.name')
    guarantor_tags = fields.Many2many(string="Tags", related='guarantor_id.category_id')
    image = fields.Binary(string='Image')
    medication_ids = fields.Many2many('dental.medication')
    chronic_conditions_ids = fields.Many2many('dental.chronic.diseases')
    allergy_ids = fields.Many2many('dental.allergies')
    habit_ids = fields.Many2many('dental.habits',string="Habits/Substance Abuse")
    hospitalised = fields.Boolean(string="Hospitalised this year?")
    female = fields.Boolean(string="FEMALE")
    pregnant = fields.Boolean(string="Are you pregnant?")
    nursing = fields.Boolean(string="Are you nursing?")
    treatment = fields.Selection([
        ('hormone_replacement_treatment','Hormone Replacement Treatment'),
        ('birth_control','Birth Control'),
        ('neither','Neither'),
    ])
    notes = fields.Char()
    special_care = fields.Char(string="Under Special Care")
    psychiatric_history = fields.Char(string="Psychiatric History")
    medical_aid_id = fields.Many2one('dental.medical.aid',string="Medical Aid")
    medical_aid_plan = fields.Char(string="Medical Aid Plan")
    medical_aid_number = fields.Char(string="Medical Aid Number")
    member_code = fields.Char(string="Main Member Code")
    dependant_code = fields.Char(string="Dependant Code")
    emergency_contact_id = fields.Many2one('res.partner',string="Emergency Contact")
    emergency_contact_phone = fields.Char(string="Mobile", related='emergency_contact_id.phone')
    history_ids = fields.One2many('dental.history','history_id',string="History")
    occupation = fields.Char(string="Occupation or Grade")
    identity_number = fields.Char(string="Identity Number")
    date_of_birth = fields.Date(string="Date of Birth")
    gender = fields.Selection([
        ('male','Male'),
        ('female','Female'),
        ('neither','Neither')
    ])
    marital_status = fields.Selection([
        ('single','Single'),
        ('married','Married'),
        ('divorced','Divorced'),
        ('widowed','Widowed')
    ])
    tags = fields.Char(string="Tags")
    company_id = fields.Many2one('res.company',string="Company")
    
    @api.onchange('state')
    def action_sold(self):
        if self.state == 'to_invoice':
            print("Invoice created")
            for record in self:
                res = {
                    "move_type": "out_invoice",
                    "partner_id": record.guarantor_id.id,
                    "invoice_line_ids": [
                        Command.create(
                        {
                            "name": record.name,
                            "quantity": 1,
                            "invoice_date": date.today(),
                            "price_unit": 100,
                        }
                    ),
                    ],
                }
            
                self.env["account.move"].sudo().create(res)
           

