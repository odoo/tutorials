import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { AwesomeDashboard } from "./awesome_dashboard";

export class AwesomeDashboardWrapper extends Component {
    static template = "awesome_dashboard.AwesomeDashboardWrapper";
    static components = { Layout, AwesomeDashboard };

    setup() {
        // If you need any services, e.g., action
        this.action = this.env.services.action;
    }

    // Move the handlers here
    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Leads",
            res_model: "crm.lead",
            views: [
                [false, "list"],
                [false, "form"],
            ],
            target: "current",
        });
    }

    get layoutProps() {
        return {
            display: {
                controlPanel: {},
                className: "o_dashboard h-100",
            },
        };
    }
}

// Register the action
try {
    registry.category("actions").add(
        "awesome_dashboard.dashboard",
        AwesomeDashboardWrapper
    );
} catch (e) {
    if (!e.message.includes("already exists")) {
        throw e;
    }
}