import { X2ManyField, x2ManyField } from "@web/views/fields/x2many/x2many_field";
import { TableRenderer } from "./table_render";
import { registry } from "@web/core/registry"

export class TableWidget extends X2ManyField {
    static components = {
        ...X2ManyField.components,
        ListRenderer: TableRenderer,
    };
}

export const tableWidget = {
    ...x2ManyField,
    component: TableWidget,
    supportedTypes: ["one2many"],
};

registry.category("fields").add("table_widget", tableWidget)
