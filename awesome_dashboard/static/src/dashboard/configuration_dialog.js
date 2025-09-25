import { useService } from "@web/core/utils/hooks";
import { Component } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";

export class ConfigurationDialog extends Component {
    static template = "awesome_dashboard.ConfigurationDialog";
    static components = { Dialog, CheckBox };
    static props = {
        items: Array,
        close: {},
        onApply: Function,
    };

    setup() {
        this.orm = useService("orm");
        this.disabledElements = this.props.items
            .filter((item) => !item.enabled)
            .map((item) => item.element.id);
    }

    onChange(id) {
        let index = this.disabledElements.indexOf(id);
        if (index === -1) {
            this.disabledElements.push(id);
            return;
        }
        this.disabledElements.splice(index, 1);
    }

    async apply() {
        await this.orm.call(
            "ir.config_parameter",
            "set_param",
            ["awesome_dashboard_config", JSON.stringify(this.disabledElements)]
        )
        this.props.onApply();
        this.props.close();
    }
}
