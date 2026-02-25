/** @odoo-module **/
import { Component } from "@odoo/owl";
import { Layout } from "@web/search/layout";
import { AwesomeDashboard } from "./awesome_dashboard";
import { registry } from "@web/core/registry";

export class AwesomeDashboardWrapper extends Component {
    static template = "awesome_dashboard.AwesomeDashboardWrapper";
    static components = { Layout, AwesomeDashboard };

    setup() {
        this.action = this.env.services.action;
        this.dashboardOpenSettings = null;

        this.setDashboardSettingsCallback = (fn) => {
            this.dashboardOpenSettings = fn;
        };
    }

    openSettings() {
        if (this.dashboardOpenSettings) {
            this.dashboardOpenSettings();
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
            views: [[false, "list"], [false, "form"]],
            target: "current",
        });
    }

    get layoutProps() {
        return { display: { controlPanel: {}, className: "o_dashboard h-100" } };
    }
}

// Register for lazy loading
registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboardWrapper);