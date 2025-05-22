/** @odoo-module **/

import { Component } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";

export class AwesomeDashboardConfigDialog extends Component {
    static template = "awesome_dashboard.AwesomeDashboardConfigDialog";
    static components = { Dialog };
    static props = { close: { type: Function, optional: true }, onConfirm: { type: Function, optional: true } };
    static defaultProps = {
        close: () => {},
        onConfirm: () => {},
    };

    setup() {
        if (localStorage.getItem("awesome_dashboard_config") === null) {
            localStorage.setItem(
                "awesome_dashboard_config",
                JSON.stringify({
                    average_quantity: { title: "Average Quantity", active: true },
                    average_time: { title: "Average Time", active: true },
                    nb_cancelled_orders: { title: "Cancelled Orders", active: true },
                    nb_new_orders: { title: "New Orders", active: true },
                    total_amount: { title: "Total Amount", active: true },
                    orders_by_size: { title: "Orders by Size", active: true },
                })
            );
        }
        this.configItems = JSON.parse(localStorage.getItem("awesome_dashboard_config"));
    }

    onSave() {
        localStorage.setItem("awesome_dashboard_config", JSON.stringify(this.configItems));
        this.props.onConfirm(this.configItems);
        this.props.close();
    }

    discard() {
        this.props.close();
    }
}
