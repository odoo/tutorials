from odoo import fields, models, api


class AddOfferProperty(models.Model):
    _name = "make.appointment"
    _description = "Make appointment"

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        props = self.env["estate.property"].browse(self.env.context["active_id"])
        res["attendes_id"] = props.salesperson
        return res

    agenda = fields.Char(required=True)
    date_from = fields.Date(
        string="Start Date",
        required=True,
        help="Start Date, included in the fiscal year.",
    )
    date_to = fields.Date(
        string="End Date",
        required=True,
        help="Ending Date, included in the fiscal year.",
    )
    organiser = fields.Many2one(
        "res.users",
        string="Organiser",
        default=lambda self: self.env.user,
        readonly=True,
    )
    attendes_id = fields.Many2one("res.users", string="Attendes Id", required=True)

    def confirm_make_appointment(self):
        vals = {
            "name": self.agenda,
            "start": self.date_from,
            "stop": self.date_to,
            "partner_id": self.attendes_id,
        }
        self.env["calendar.event"].create(vals)
        pass
