
/** @odoo-module **/

import { registry } from "@web/core/registry";
import { ListRenderer } from "@web/views/list/list_renderer";
import { X2ManyField, x2ManyField } from "@web/views/fields/x2many/x2many_field";


export class KitListRenderer extends ListRenderer {
    setup() {
        super.setup();
    }

    getRowClass(record) {
        const existingClasses = super.getRowClass(record);
        return record.data.parent_id ? `${existingClasses} o_readonly_row` : existingClasses;
    }
}


export class KitFieldOne2Many extends X2ManyField {}
KitFieldOne2Many.components = {
    ...X2ManyField.components,
    ListRenderer: KitListRenderer,
};


export const kitFieldOne2Many = {
    ...x2ManyField,
    component: KitFieldOne2Many,
    additionalClasses: [...x2ManyField.additionalClasses || [], "o_field_one2many"],  
};

registry.category("fields").add("kit_one2many", kitFieldOne2Many);
