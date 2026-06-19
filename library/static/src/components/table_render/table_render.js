import { Component } from "@odoo/owl";

export class TableRenderer extends Component {
    static template = "library.TableRenderer";
    static props = {
        list: { type: Object },
        activeActions: { type: Object, optional: true },
        openRecord: { type: Function, optional: true },
        onAdd: { type: Function, optional: true },
        readonly: { type: Boolean, optional: true },
        archInfo: { type: Object, optional: true },
        editable: { type: String, optional: true },
        cycleOnTab: { type: Boolean, optional: true },
        nestedKeyOptionalFieldsData: { type: Object, optional: true },
        hasOpenFormViewButton: { type: Boolean, optional: true },
        onOpenFormView: { type: Function, optional: true },
    }

    get values() {
        return this.props.list.records || []
    }

    getStatusColor(status) {
        return { returned: "#22c55e", overdue: "#ef4444" }[status] || "#f59e0b";
    }

    getStatusLabel(status) {
        return { returned: "Returned", overdue: "Overdue" }[status] || "Borrowed";
    }

    formatDate(dateStr) {
        if (!dateStr) return "—";
        return new Date(dateStr).toLocaleDateString("en-IN", {
            day: "2-digit", month: "short", year: "numeric"
        });
    }

    openRecord = (record) => {
        this.props.openRecord?.(record);
    }

    addRecord = () => {
        this.props.onAdd?.({ editable: true });
    }

}
