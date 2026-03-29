/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class DashboardSettings extends Component {
    static template = "awesome_dashboard.DashboardSettings";

    setup() {
        this.state = useState({
            hidden: new Set(this.props.hiddenItems),
        });
    }

    toggle(id) {
        if (this.state.hidden.has(id)) {
            this.state.hidden.delete(id);
        } else {
            this.state.hidden.add(id);
        }
    }

    apply() {
        const hiddenItems = Array.from(this.state.hidden);
        localStorage.setItem("dashboard_hidden", JSON.stringify(hiddenItems));
        this.props.close();
        location.reload();   
    }
}
