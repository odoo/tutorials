import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { _t } from "@web/core/l10n/translation";


export class DashboardConfiguration extends Component {
    static template = "awesome_dashboard.DashboardConfiguration";
    static components = { Dialog };
    static props = {
        close: Function,
        items: Object,
        hiddenItems: Array,
        onSave: Function,
    };

    setup() {
        const allItems = Object.entries(this.props.items);

        this.state = useState({
            selectedItems: {}
        });

        allItems.forEach(([itemId, item]) => {
            this.state.selectedItems[item.backend_attribute] = !this.props.hiddenItems.includes(item.backend_attribute);
        });
    }

    toggleItem(backendAttribute) {
        this.state.selectedItems[backendAttribute] = !this.state.selectedItems[backendAttribute];
    }

    onApply() {
        const hiddenItems = Object.entries(this.state.selectedItems)
            .filter(([backendAttribute, isVisible]) => !isVisible)
            .map(([backendAttribute]) => backendAttribute);

        this.props.onSave(hiddenItems);
        this.props.close();
    }

    getItemDescription(item) {
        return item.description || _t("Dashboard item");
    }
}
