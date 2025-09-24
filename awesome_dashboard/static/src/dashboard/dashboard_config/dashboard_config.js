import { Component } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";

export class DashboardConfig extends Component {
    static template = "awesome_dashboard.DashboardConfig";
    static components = { Dialog };
    static props = {
        items: Object,
        applyFunction: Function,
        disabledItems: Array,
        close: Function
    }

    setup() {
        this.disabledItems = this.props.disabledItems.slice();

        this.onChange = (ev, item_id) => {
            if (ev.target.checked) {
                const index = this.disabledItems.indexOf(item_id);
                if (index >= 0) {
                    this.disabledItems.splice(index, 1);
                }
            } else {
                this.disabledItems.push(item_id);
            }
        }
    }

    onApply() {
        this.props.applyFunction(this.disabledItems);
        this.props.close();
    }
}
