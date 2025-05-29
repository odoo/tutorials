from odoo import api, models


class PosSession(models.Model):
    _inherit = "pos.session"

    @api.model
    def _load_pos_data_models(self, config_id):
        data = super()._load_pos_data_models(config_id)
        data.append("hr.employee")
        return data

    @api.model
    def _pos_data_process_lines(self, lines):
        lines = super()._pos_data_process_lines(lines)

        # Optimize employee data for POS
        if lines.get("hr.employee"):
            # Only load necessary employee fields to improve performance
            needed_fields = [
                "id",
                "name",
                "user_id",
                "department_id",
                "job_title",
                "work_phone",
            ]

            # Pre-sort employees by name for better UX
            lines["hr.employee"] = sorted(
                lines.get("hr.employee", []), key=lambda emp: emp.get("name", ""),
            )

            # Filter only needed fields
            for i, emp in enumerate(lines.get("hr.employee", [])):
                lines["hr.employee"][i] = {
                    k: v for k, v in emp.items() if k in needed_fields
                }

        return lines
