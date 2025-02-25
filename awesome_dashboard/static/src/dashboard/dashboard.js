/** @odoo-module **/

import { Component, useState, onMounted, onWillUnmount } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { rpc } from "@web/core/network/rpc";
import { DashboardItem } from "./dashboard_item";
import { items } from "./dashboard_items";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem };

    setup() {
        this.layoutProps = { controlPanel: {} };
        this.action = useService("action");
        this.state = useState({
            statistics: {},
        });
        this.items = items;

        this.fetchData();

        this.intervalId = null;
        onMounted(() => {
            this.intervalId = setInterval(() => {
                this.fetchData();
            }, 1000);
        });

        onWillUnmount(() => {
            if (this.intervalId) {
                clearInterval(this.intervalId);
            }
        });
    }

    async fetchData() {
        const result = await rpc("/awesome_dashboard/statistics", {});
        if (result) {
            this.state.statistics = result;
        }
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Leads",
            res_model: "crm.lead",
            view_mode: "kanban,tree,form",
            views: [[false, "kanban"], [false, "list"], [false, "form"]],
            target: "current",
        });
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
