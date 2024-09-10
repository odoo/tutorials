from odoo import http
from odoo.http import request


class DentalController(http.Controller):
    # show dental on my account
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

    # show all patient
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

    # show personal detail
    @http.route(
        ["/personal/detail/<int:record_id>"],
        type="http",
        auth="public",
        website=True,
    )
    def show_personal_detail(self, record_id, **kwargs):
        data = request.env["dental.patients"].sudo().browse(record_id)
        return request.render(
            "dental.personal_detail_template",
            {
                "personal": data,
            },
        )

    # show medical Aid detail
    @http.route(
        ["/patients/medical_aid/detail/<int:record_id>"],
        type="http",
        auth="public",
        website=True,
    )
    def show_medical_aid_detail(self, record_id, **kwargs):
        data = request.env["dental.patients"].sudo().browse(record_id)
        medical_aid_id = data.medical_aid_id.id
        medical_aid = (
            request.env["medical.aids"]
            .sudo()
            .search(
                [
                    ("id", "=", medical_aid_id),
                ],
            )
        )
        return request.render(
            "dental.medical_aid_detail_template",
            {
                "medical_aid": medical_aid,
                "patient": data,
            },
        )

    # medical history
    @http.route(
        ["/medical/history/<int:patient_id>"],
        type="http",
        auth="public",
        website=True,
    )
    def show_medical_history(self, patient_id, **kwargs):
        data = request.env["dental.patients"].sudo().browse(patient_id)
        history_id = data.history_id
        return request.render(
            "dental.portal_medical_history_template",
            {"history": history_id, "patient": data},
        )

    # dental history
    @http.route(
        ["/dental/history/<int:patient_id>"],
        type="http",
        auth="public",
        website=True,
    )
    def show_dental_history(self, patient_id, **kwargs):
        data = request.env["dental.patients"].sudo().browse(patient_id)
        history_id = data.history_id
        return request.render(
            "dental.dental_history_view",
            {
                "history": history_id,
                "patient": data,
            },
        )

    # Dental_history_detail
    @http.route(
        ["/history/detail/<int:history_id>/<int:patient_id>"],
        type="http",
        auth="public",
        website=True,
    )
    def show_dental_history_detail(self, history_id, patient_id, **kwargs):
        patient = request.env["dental.patients"].sudo().browse(patient_id)
        data = request.env["pateint.history"].sudo().browse(history_id)
        return request.render(
            "dental.dental_history_detail_view",
            {
                "history": data,
                "patient": patient,
            },
        )
