/** @odoo-module **/

import { registry } from "@web/core/registry";
import { ListRenderer } from "@web/views/list/list_renderer";
import { X2ManyField, x2ManyField } from "@web/views/fields/x2many/x2many_field";


export class HideRemoveListRenderer extends ListRenderer {
    static recordRowTemplate = "crm_contact_details.HideRemoveListRenderer.RecordRow";
}

export class HideRemoveX2Many extends X2ManyField {
    static components = {
        ...X2ManyField.components,
        ListRenderer: HideRemoveListRenderer,
    };
}

export const hideRemoveX2Many = {
    ...x2ManyField,
    component: HideRemoveX2Many,
};

registry.category("fields").add("hide_remove_x2many", HideRemoveX2Many);
