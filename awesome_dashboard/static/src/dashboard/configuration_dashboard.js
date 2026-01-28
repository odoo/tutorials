import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";

export class ConfigurationDashboard extends Component {
    static template = "awesome_dashboard.ConfigurationDashboard";
    static components = {
        Dialog,
        CheckBox,
    };
    static props = ["close", "items", "disabledItems", "onApply"];

    setup() {
        this.items = useState(
            this.props.items.map((item) => ({
                ...item,
                enabled: !this.props.disabledItems.includes(item.id),
            }))
        );
    }

    onApply() {
        const disabledItems = this.items.filter((item) => !item.enabled).map((item) => item.id);
        this.props.onApply(disabledItems);
        this.props.close();
    }
}
