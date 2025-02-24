import { Component, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboardItem";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem };

    setup() {
        // Services
        this.notification = useService("notification");
        this.sharedState = useService("shared_state");
        this.action = useService("action");
        this.statisticService = useService("awesome_dashboard.statistics");

        // Shared state usage
        this.sharedState.setValue("username", "Tushar");
        const username = this.sharedState.getValue("username");
        console.log(`Hello ${username}`);

        // Statistics loading with caching
        this.statistics = {};
        onWillStart(async () => {
            this.statistics = await this.statisticService.loadStatistics();
            console.log(this.statistics);
        });
    }

    openSetting() {
        this.action.doAction("base_setup.action_general_configuration");
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Leads",
            res_model: "crm.lead",
            target: "current",
            views: [[false, "list"], [false, "form"]],
        });
    }
}

// Custom Notification Service
const myservices = {
    dependencies: ["notification"],
    start(env, { notification }) {
        let counter = 1;
        setInterval(() => {
            notification.add(`Tick Tock ${counter++}`);
        }, 5000);
        return {};
    },
};

// Shared State Service
const sharedStateService = {
    start(env) {
        let state = {};
        return {
            getValue(key) {
                return state[key];
            },
            setValue(key, value) {
                state[key] = value;
            },
        };
    },
};

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
registry.category("services").add("myservices", myservices);
registry.category("services").add("shared_state", sharedStateService);
