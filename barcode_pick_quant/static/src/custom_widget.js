import { registry } from "@web/core/registry";
import { X2ManyField, x2ManyField } from "@web/views/fields/x2many/x2many_field";

export class CustomWidget extends X2ManyField {
    setup() {
        super.setup();
    }

    /**
     * Opens a record and updates the related fields if available.
     * @param {Object} record - The record to be opened.
     */
    async openRecord(record) {
        if (!record?.data?.location_id) return;

        // Update only if the new record has values, otherwise retain existing values
        this.props.record.update({
            location_id: record.data.location_id || this.props.record.data.location_id,
            lot_id: record.data.lot_id || this.props.record.data.lot_id,
            package_id: record.data.package_id || this.props.record.data.package_id,
            owner_id: record.data.owner_id || this.props.record.data.owner_id,
        });

        // Save the updated record
        this.props.record.save();
    }
}

export const customWidget = {
    ...x2ManyField,
    component: CustomWidget,
};

registry.category("fields").add("custom_widget", customWidget);
