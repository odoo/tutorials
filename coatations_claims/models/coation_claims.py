import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import ValidationError

class CoationsClaims(models.Model):
    _name = "coatations.claims"
    _description = "List of all coations"
    name = fields.Char(
        string="Order Reference",
        required=True,
        copy=False,
        readonly=True,
        index="trigram",
        default=lambda self: ("New"),
    )
    partner_id = fields.Many2one("res.partner",required=True)
    client_id = fields.Many2one("res.partner",required=True)
    reseller_id = fields.Many2one("res.partner", string="Reseller", readonly=False,required=True)
    date_from = fields.Date(default=lambda self: fields.Datetime.today(),required=True)
    date_to = fields.Date(required=True,default=lambda self: fields.Datetime.today() + relativedelta(months=3))
    state = fields.Selection(
        string="state",
        selection=[("new", "New"), ("active", "Active"), ("expired", "Expired")],
        default="new",
        compute="_compute_state"
    )
    coation_lines_ids = fields.One2many("coatations.lines", "coation_id")
    sale_order_ids = fields.Many2many("sale.order")
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "New") == "New":
                year = datetime.datetime.now().year
                sequence = self.env["ir.sequence"].next_by_code(self.id) or "0000"
                vals["name"] = f"COT/{year}/{sequence}"

        return super(CoationsClaims, self).create(vals)

    @api.constrains("date_from", "date_to")
    def _check_date_range(self):
        for record in self:
            if record.date_from and record.date_to:
                if record.date_to < record.date_from:
                    raise ValidationError(
                        "The 'Date To' cannot be earlier than 'Date From'. Please correct the dates."
                    )
    
    @api.depends('coation_lines_ids.status')
    def _compute_state(self):
        for record in self:
            # Flag to track the state of the lines
            has_active = False
            has_expired = False
            
            # Loop through the coation_lines_ids to check the status
            for line in record.coation_lines_ids:
                if line.status == 'active':
                    has_active = True
                elif line.status == 'expired':
                    has_expired = True
            
            # Get today's date using fields.Date.today() since 'date_to' is a Date field
            today = fields.Date.today()

            # Compute the state based on today's date and the line statuses
            if today < record.date_to:
                if not (has_active or has_expired):
                    record.state = "new"
                elif has_active:
                    record.state = "active"
                elif has_expired:
                    record.state = "expired"
            else:
                record.state = "expired"