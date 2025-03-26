/** @odoo-module **/

import { Component , watch } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { onWillStart, useState } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";
import { PieChart } from "./pie_chart/pie_chart";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout , DashboardItem , PieChart };

    setup() {
        this.action = useService("action");
        this.statistics = useService("awesome_dashboard.loadStatistics");

        this.state = useState({
            stats: {},
            sizes: [],
            quantities: [],
        });


        onWillStart(async () => {
            await this._updateStatistics();
        });
    }

    async _updateStatistics() {
        if (this.statistics.isReady) {
            console.log("Updated Statistics Data:", this.statistics);

            this.state.stats = { ...this.statistics };

            this.state.sizes = Object.keys(this.statistics.orders_by_size || {});
            this.state.quantities = Object.values(this.statistics.orders_by_size || {});
        }
    }
    
    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            res_model: "crm.lead",
            views: [[false, "kanban"], [false, "list"], [false, "form"]],
            target: "current",
        });
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
