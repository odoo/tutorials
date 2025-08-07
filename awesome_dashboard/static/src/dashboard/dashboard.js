/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "../dashboard_item/dashboard_item";
import { PieChart } from "./PieChartCard/pie_chart";
import { Component, useState } from "@odoo/owl";
import { DashboardDialog } from "../dashboard_dialog/dashboard_dialog";
import { browser } from "@web/core/browser/browser";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PieChart, DashboardDialog };

    setup() {
        this.action = useService("action");
        this.dialog = useService("dialog");
        this.statistics = useService("awesome_dashboard.statistics");
        this.result = useState(this.statistics.stats);
        this.state = useState({ metricConfigs: {} });
        this.items = registry.category("awesome_dashboard_cards").get("awesome_dashboard.Cards");
        this.getBrowserCookie();
    }

    openDialog() {
        this.dialog.add(DashboardDialog, {
            metrics: this.items,
            metricConfigs: this.state.metricConfigs,
            closeDialog: this.closeDialog.bind(this),
            updateMetricConfigCallback: this.updateMetricConfig.bind(this)
        });
    }

    closeDialog() {
        this.getBrowserCookie();
    }

    updateMetricConfig(updated_metricConfig) {
        this.state.metricConfigs = updated_metricConfig;
        this.setBrowserCookie();
    }

    setBrowserCookie() {
        browser.localStorage.setItem(
            "awesome_dashboard.metric_configs", JSON.stringify(this.state.metricConfigs)
        );
    }

    getBrowserCookie() {
        const metric_cookie_data = browser.localStorage.getItem("awesome_dashboard.metric_configs");
        if (metric_cookie_data) {
            this.state.metricConfigs = JSON.parse(metric_cookie_data);
        } else {
            const initialMetricState = {};
            for (const metric of this.items) {
                initialMetricState[metric.id] = true;
            }
            this.state.metricConfigs = initialMetricState;
        }
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: _t('Leads'),
            target: 'current',
            res_model: 'crm.lead',
            views: [[false, 'kanban'], [false, 'list'], [false, 'form']], // [view_id, view_type]
        });
    }
}

registry.category("lazy_components").add("awesome_dashboard.LazyComponent", AwesomeDashboard);
