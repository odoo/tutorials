/** @odoo-module **/

import { Component, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./item/item";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem };

    static props = {
        stats: {
            type: Object,
            optional: true,
        },
    }

    setup() {
        this.display = {
            controlPanel: {},
        };
        this.action = useService("action");
        this.statistics = useService("awesome_dashboard.statistics");
        onWillStart(async () => {
            this.props.stats = await this.statistics.loadStatistics();
            console.log(this.props.stats);
        })
    }

    openCustomerKanbanView() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction("crm.crm_lead_all_leads");
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
