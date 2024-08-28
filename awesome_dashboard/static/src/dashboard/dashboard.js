/** @odoo-module **/

import {Component, reactive, useState} from "@odoo/owl";
import {DashboardItem} from "./dashboardItem/dashboardItem";
import {_t} from "@web/core/l10n/translation";
import {Layout} from "@web/search/layout"
import {useService} from "@web/core/utils/hooks";
import {registry} from "@web/core/registry";


class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = {Layout, DashboardItem}

    setup() {
        this.display = {controlPanel: {}};
        this.items = registry.category("awesome_dashboard").getAll();
        this.action = useService("action");
        this.statistics = useState(useService("statistics"));
    }

    customersAction() {
        this.action.doAction("base.action_partner_form")
    }

    async openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: _t("CRM Leads"),
            res_model: "crm.lead",
            views: [[false, 'tree']],
        })
    }
}

const statistics = {
    dependencies: ["rpc"],
    start(env, {rpc}) {
        let statistics = reactive({value: null})
        loadStatistics()

        async function loadStatistics() {
            statistics.value = await rpc("/awesome_dashboard/statistics")
        }

        setInterval(loadStatistics, 5 * 1000)
        return statistics;
    },
};

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
registry.category("services").add("statistics", statistics);
