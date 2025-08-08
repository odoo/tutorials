import { registry } from "@web/core/registry";
import { X2ManyField, x2ManyField } from "@web/views/fields/x2many/x2many_field";


export class BarcodeQuantOne2Many extends X2ManyField {
    async openRecord(record) {
        // Update only if the new record has values, otherwise retain existing values
        this.props.record.update({
            location_id: record.data.location_id || this.props.record.data.location_id,
            lot_id: record.data.lot_id || this.props.record.data.lot_id,
            package_id: record.data.package_id || this.props.record.data.package_id,
            owner_id: record.data.owner_id || this.props.record.data.owner_id,
        });
    }
}

export const barcodeQuantOne2Many = {
    ...x2ManyField,
    component: BarcodeQuantOne2Many,
};

registry.category("fields").add("barcode_quant_one_2_many", barcodeQuantOne2Many);
