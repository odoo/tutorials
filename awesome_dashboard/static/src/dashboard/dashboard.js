/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { PieChart } from "./dashboard_pie_chart/dashboard_pie_chart";
import { DashboardConfig } from "./dashboard_config/dashboard_config";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PieChart };
    static props = ['*'];

    setup() {
        this.action = useService("action");
        this.title = _t("Awesome Dashboard");
        this.statistics = useState(useService("awesome_dashboard.statistics"));
        this.items = registry.category("awesome_dashboard.items").getAll();
        this.dialog = useService("dialog");
        this.state = useState({
            disabledItems: localStorage.getItem("disabledItems") ? localStorage.getItem("disabledItems").split(",") : []
        });
    }

    openCustomers = () => {
        this.action.doAction("base.action_partner_form");
    }

    openLeads = () => {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: _t('Leads'),
            res_model: 'crm.lead',
            views: [[false, 'list'], [false, 'form']],
            target: 'current',
        })
    }

    openDashboardConfig = () => {
        this.dialog.add(DashboardConfig, {
            items: this.items,
            applyFunction: this.onApplyConfiguration.bind(this),
            disabledItems: this.state.disabledItems
        });
    }

    onApplyConfiguration = (ids) => {
        this.state.disabledItems = ids;
        localStorage.setItem("disabledItems", ids);
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
