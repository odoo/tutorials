/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { Component, useState, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item";
import { PieChart } from "./pie_chart/pie_chart";
import { ConfigurationDialog } from "./configuration_dialog";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PieChart };

    setup() {
        this.action = useService("action");
        this.orm = useService("orm");
        this.statistics = useService("awesome_dashboard.statistics");
        this.state = useState({ items: [], stats: this.statistics });
        this.dialog = useService("dialog");

        onWillStart(async () => await this.updateDashboard())
    }

    async updateDashboard() {
        const config = await this.orm.call(
            "ir.config_parameter",
            "get_param",
            ["awesome_dashboard_config"]);
        const disabledElements = JSON.parse(config)
        this.state.items = registry
            .category("awesome_dashboard")
            .getAll()
            .filter((el) => !disabledElements.some((e) => e == el.id));
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: _t("Leads"),
            res_model: "crm.lead",
            views: [
                [false, "list"],
                [false, "form"],
            ],
        });
    }

    customizeDashboard() {
        let all = registry.category("awesome_dashboard").getAll();

        this.dialog.add(ConfigurationDialog, {
            items: all.map(item => ({
                element: item,
                enabled: this.state.items.some((element) => item.id == element.id)
            }))
            ,
            onApply: this.updateDashboard.bind(this),
        });
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
