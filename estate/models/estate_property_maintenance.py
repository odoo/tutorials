from odoo import models,fields,api
from odoo.exceptions import UserError

class EstatePropertyMaintenance(models.Model):

    _name = "estate.property.maintenance"
    _description = "Estate Property Maintenance"
    _order = "create_date asc"

    title = fields.Char(string="title", required=True)
    description = fields.Text(string="Description",required=True)
    maintenance_category = fields.Selection(
        selection=[
            ('electrical',"Electrical"),
            ('plumbing',"Plumbing"),
            ('room_cleaning',"Room Cleaning"),
            ('washroom_cleaning',"Washroom Cleaning"),
            ('carpenter',"Carpentry"),
            ('other',"Other"),
        ],
        string="Category",
        copy=False,
        required=True
    )
    custom_category=fields.Char(string="Custom Category")

    @api.onchange('maintenance_category')
    def _onchange_maintenance_category(self):
        if self.maintenance_category != 'other':
            self.custom_category = False

    property_id = fields.Many2one(
        'estate.property',
        required = True,
        string="propert name")
    inspection_date=fields.Date (string="Date Of Inspection", required=True)
    expected_price=fields.Float (string="Expected Cost")
    scheduled_date=fields.Date(string="Scheduled Date")

    @api.constrains('inspection_date','scheduled_date')
    def _check_scheduled_date(self):
        for record in self:
            if record.scheduled_date < record.inspection_date:
               raise UserError("scheduled date can not be before inspection date")
    
    responsible_id = fields.Many2one("res.users",string="responsible",default =lambda self:self.env.user)
    actual_cost = fields.Float(string="Actual Cost")
    state = fields.Selection(
        selection=[
            ('new',"New"),
            ('started',"Started"),
            ('in_progress',"In Progress"),
            ('completed',"Completed"),
        ],string="state"
    )
    