from odoo import fields, models


class BusinessTrip(models.Model):
    _name = "business.trip"
    _inherit = ["mail.thread"]
    _description = "Business Trip"

    name = fields.Char(tracking=True)
    partner_id = fields.Many2one("res.partner", "Responsible", tracking=True)
    guest_ids = fields.Many2many("res.partner", "Participants")
    state = fields.Selection(
        [("draft", "New"), ("confirmed", "Confirmed")], tracking=True
    )

    def _track_subtype(self, init_values):
        self.ensure_one()
        if "state" in init_values and self.state == "confirmed":
            return self.env.ref("estate.mt_state_change")
        return super()._track_subtype(init_values)
