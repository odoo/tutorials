from odoo import http
from odoo.http import request


class DentalController(http.Controller):

    @http.route("/dental", auth="public", website=True)
    def display_patients(self):
        current_user = request.env.user
        patients = request.env["dental.patient"].search(
            [("guarantor_id", "=", current_user.partner_id.id)]
        )
        return request.render("dental.dental_patient_page", {"patients": patients})

    @http.route("/dental/<string:patient_name>", auth="public", website=True)
    def display_patient_details(self, patient_name):
        patient = (
            request.env["dental.patient"]
            .sudo()
            .search([("name", "=", patient_name)], limit=1)
        )

        if not patient:
            return request.not_found()

        return request.render(
            "dental.dental_patient_details_page", {"patient": patient}
        )

    @http.route(
        "/dental/<string:patient_name>/personal",
        type="http",
        auth="public",
        website=True,
    )
    def render_dental_patient_form(self, patient_name):
        patient = (
            request.env["dental.patient"]
            .sudo()
            .search([("name", "=", patient_name)], limit=1)
        )
        return request.render(
            "dental.dental_patient_form_template",
            {
                "patient": patient,
            },
        )

    @http.route(
        "/dental/<string:patient_name>/medical_history",
        type="http",
        auth="public",
        website=True,
    )
    def dental_history_list_view(self, patient_name):
        patient = (
            request.env["dental.patient"]
            .sudo()
            .search([("name", "=", patient_name)], limit=1)
        )
        return request.render(
            "dental.patient_details_controller_appointment",
            {
                "patients": patient.history_ids,
            },
        )
