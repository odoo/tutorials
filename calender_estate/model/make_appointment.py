from odoo import api, fields, models


class Make_appointment(models.TransientModel):
    _name = "make.appointment"
    _description = "make an appointment"

    name = fields.Char(required=True)
    description = fields.Char()
    start_date = fields.Datetime("Start date", required=True)
    end_date = fields.Datetime("End date", required=True)
    orgniser = fields.Many2one(
        "res.users", "Organizer", default=lambda self: self.env.user, readonly=True
    )
    attendes_id = fields.Many2one("res.users", string="Attendes_id", required=True)

    @api.model
    def default_get(self, fields_list):
        result = super().default_get(fields_list)
        active_id = self.env.context.get("active_id", [])
        current_property = self.env["estate.property"].browse(active_id)
        result["attendes_id"] = current_property.salesperson_id
        return result

    def make_appointment(self):
        self.env["calendar.event"].create(
            {
                "name": self.name,
                "start": self.start_date,
                "stop": self.end_date,
                "partner_id": self.attendes_id,
            }
        )
