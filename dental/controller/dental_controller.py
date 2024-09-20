from odoo import http
from odoo.http import request


class DentalController(http.Controller):

    @http.route(
        ["/home/dental", "/home/dental/page/<int:page>"], auth="public", website=True
    )
    def display_patients(self, page=1):
        patients_per_page = 4
        current_user = request.env.user

        total_patients = (
            request.env["dental.patient"]
            .sudo()
            .search_count([("guarantor_id", "=", current_user.partner_id.id)])
        )

        pager = request.website.pager(
            url="/home/dental",
            total=total_patients,
            page=page,
            step=patients_per_page,
        )

        patients = (
            request.env["dental.patient"]
            .sudo()
            .search(
                [("guarantor_id", "=", current_user.partner_id.id)],
                offset=pager["offset"],
                limit=patients_per_page,
            )
        )

        return request.render(
            "dental.dental_patient_page", {"patients": patients, "pager": pager}
        )

    @http.route("/home/dental/<int:record_id>", auth="public", website=True)
    def display_patient_details(self, record_id):
        patient = request.env["dental.patient"].sudo().browse(record_id)

        if not patient:
            return request.not_found()

        return request.render(
            "dental.dental_patient_details_page", {"patient": patient}
        )

    @http.route(
        "/home/dental/<int:record_id>/personal",
        type="http",
        auth="public",
        website=True,
    )
    def render_dental_patient_form(self, record_id):
        patient = request.env["dental.patient"].sudo().browse(record_id)
        return request.render(
            "dental.dental_patient_personal_details",
            {
                "patient": patient,
            },
        )

    @http.route("/home/dental/<int:record_id>/medical_aid", auth="user", website=True)
    def medical_aid_details(self, record_id):
        patient = http.request.env["dental.patient"].sudo().browse(record_id)
        return http.request.render(
            "dental.dental_patient_medical_aid_details",
            {
                "patient": patient,
            },
        )

    @http.route(
        "/home/dental/<int:record_id>/medical_history",
        type="http",
        auth="public",
        website=True,
    )
    def medical_history_view(self, record_id):
        patient = request.env["dental.patient"].sudo().browse(record_id)
        return request.render(
            "dental.dental_history_list_view",
            {
                "patients": patient.history_ids,
            },
        )

    @http.route(
        "/home/dental/<int:record_id>/appointment",
        type="http",
        auth="public",
        website=True,
    )
    def dental_history_list_view(self, record_id):
        patient = request.env["dental.patient"].sudo().browse(record_id)
        return request.render(
            "dental.patient_details_controller_appointment",
            {
                "patients": patient.history_ids,
            },
        )
