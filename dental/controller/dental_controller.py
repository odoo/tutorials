from odoo import http
from odoo.http import request


class DentalController(http.Controller):

    @http.route(
        [
            "/dental",
        ],
        type="http",
        auth="public",
        website=True,
    )
    def show_all_the_data(self, page=1, **kwargs):
        user = request.env.user
        try:
            page = int(page)
        except ValueError:
            page = 1
        patient = request.env["dental.patients"].sudo()
        patient_per_page = 6
        total_patients = patient.search_count(
            [
                ("guarantor_id", "=", user.partner_id.id),
            ]
        )
        total_pages = (total_patients + patient_per_page - 1) // patient_per_page
        page = max(1, min(page, total_pages))
        offset = (page - 1) * patient_per_page
        patients = patient.search(
            [
                ("guarantor_id", "=", user.partner_id.id),
            ],
            limit=patient_per_page,
            offset=offset,
        )
        return request.render(
            "dental.dental_patient_view_controller",
            {
                "patients": patients,
                "page": page,
                "total_pages": total_pages,
            },
        )

    @http.route(
        ["/patient/<int:record_id>"],
        type="http",
        auth="public",
        website=True,
    )
    def show_patient_details(self, record_id, **kwargs):
        data = request.env["dental.patients"].sudo().browse(record_id)
        return request.render(
            "dental.patient_details_view_controller",
            {
                "patients": data,
            },
        )

    @http.route(
        ["/dental/history/<int:patient_id>"],
        type="http",
        auth="public",
        website=True,
    )
    def show_dental_history(self, patient_id, **kwargs):
        data = request.env["dental.patients"].sudo().browse(patient_id)
        return request.render(
            "dental.dental_history_view",
            {
                "patients": data,
            },
        )
