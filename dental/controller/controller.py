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
        total_patients = request.env["dental.patient"].search_count(
            [("guarantor", "=", current_user.id)]
        )

        pager = request.website.pager(
            url="/home/dental",
            total=total_patients,
            page=page,
            step=4,
        )
        patients = request.env["dental.patient"].search(
            [("guarantor", "=", current_user.id)], limit=3, offset=pager["offset"]
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

        patient_record = request.env["dental.patient"].browse(record_id)
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
        patient_records = request.env["dental.patient"].browse(patient_id)
        history_records = patient_records.history_ids

        return request.render(
            "dental.dental_patient_history_details",
            {"history_records": history_records},
        )
