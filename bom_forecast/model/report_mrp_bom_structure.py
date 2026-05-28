from odoo import _, models


class ReportMrpReportBomStructure(models.AbstractModel):
    _inherit = "report.mrp.report_bom_structure"

    def _get_bom_data(self, *args, **kwargs):
        result = super()._get_bom_data(*args, **kwargs)

        self._set_ready_to_produce_status(result)
        self._set_forecast_status_display(result)

        return result

    def _set_ready_to_produce_status(self, line):
        if line.get("level") != 0:
            return

        qty = int(line.get("producible_qty") or 0)
        line["status"] = _("%(qty)s Ready To Produce", qty=qty) if qty > 0 else False

    def _set_forecast_status_display(self, line):
        availability_display = line.get("availability_display") or ""
        availability_state = line.get("availability_state")

        line["forecast_status_display"] = availability_display

        if availability_state in ("expected", "estimated") and availability_display:
            display_parts = availability_display.split(" ", 1)
            date_part = display_parts[1] if len(display_parts) > 1 else ""

            label = _("Estimated") if line.get("level") == 0 else _("Expected")
            line["forecast_status_display"] = _(
                "%(label)s %(date)s",
                label=label,
                date=date_part,
            )

        for child_line in line.get("components", []) + line.get("operations", []):
            self._set_forecast_status_display(child_line)
