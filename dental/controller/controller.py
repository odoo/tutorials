from odoo.http import request, route, Controller


class dentalController(Controller):
    @route(
        ["/home/dental", "/home/dental/page/<int:page>"],
        type="http",
        auth="public",
        website="True",
    )
    def dental_patient(self, **kwarg):
        current_user = request.env.user
        page = int(kwarg.get("page", 1))
        total_patients = request.env["dental.patient"].sudo().search_count(
            [("guarantor", "=", current_user.id)]
        )

        pager = request.website.pager(
            url="/home/dental",
            total=total_patients,
            page=page,
            step=4,
        )
        patients = request.env["dental.patient"].sudo().search(
            [("guarantor", "=", current_user.id)], limit=4, offset=pager["offset"]
        )

        return request.render(
            "dental.all_dental_patients_card", {"patients": patients, "pager": pager}
        )

    @route(
        "/home/dental/<int:record_id>",
        type="http",
        auth="user",
        website="True",
    )
    def patient_details(self, record_id, **kwarg):

        patient_record = request.env["dental.patient"].sudo().browse(record_id)
        return request.render(
            "dental.dental_patient_detail_card", {"patient_record": patient_record}
        )

    @route(
        "/home/dental/history/<int:patient_id>",
        type="http",
        auth="user",
        website="True",
    )
    def history_details(self, patient_id, **kwarg):
        patient_records = request.env["dental.patient"].sudo().browse(patient_id)
        history_records = patient_records.history_ids

        return request.render(
            "dental.dental_patient_history_details",
            {"history_records": history_records},
        )

    @route(
        "/home/dental/personal/<int:patient_id>", type="http", auth="user", website=True
    )
    def dental_patient_personal_details(self, patient_id, **kwarg):
        patient = request.env["dental.patient"].sudo().browse(patient_id)
        return request.render(
            "dental.dental_patient_personal_details", {"patient": patient}
        )

    @route(
        "/home/dental/medicalhistory/<int:patient_id>",
        type="http",
        auth="user",
        website=True,
    )
    def dental_patient_medical_history1(self, patient_id, **kwarg):
        patient = request.env["dental.patient"].sudo().browse(patient_id)
        medical_history = patient.history_ids
        return request.render(
            "dental.dental_patient_medical_history",
            {"medical_history": medical_history},
        )

    @route(
        "/home/dental/medicalaids/<int:patient_id>",
        type="http",
        auth="user",
        website=True,
    )
    def dental_patient_medical_aids(self, patient_id, **kwarg):
        patient = request.env["dental.patient"].sudo().browse(patient_id)
        medical_aid = patient.medical_aids_ids
        return request.render(
            "dental.dental_patient_medical_aids", {"medical_aid": medical_aid}
        )

    @route(
        "/home/dental/history/<int:patient_id>", type="http", auth="user", website=True
    )
    def dental_patient_medical_history(self, patient_id, **kwarg):
        patient = request.env["dental.patient"].sudo().browse(patient_id)
        dental_history = patient.history_ids
        return request.render(
            "dental.dental_patient_dental_history", {"dental_history": dental_history}
        )

    @route(
        "/home/dental/history/form/<int:history_id>",
        type="http",
        auth="user",
        website=True,
    )
    def dental_patient_medical_history_form_view(self, history_id, **kwarg):
        history = request.env["dental.history"].sudo().browse(history_id)

        return request.render(
            "dental.dental_patient_medical_history_form_view", {"history": history}
        )
