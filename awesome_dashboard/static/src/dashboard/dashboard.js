/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from '@web/search/layout'
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { PieChart } from "../pie_chart/pie_chart";
import { DialogFilter } from "./dialog_filter/dialog_filter";


class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PieChart, DialogFilter }

    setup() {
        this.action = useService("action");
        this.dialog = useService("dialog");
        this.statisticService = useService("awesome_dashboard.statistics");
        this.statisticService.loadStatistics('/awesome_dashboard/statistics')
        this.statistics = useState(this.statisticService.getState());
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            target: 'current',
            res_model: 'crm.lead',
            views: [[false, 'form']],
        });
    }

    openSettings() {
        this.dialog.add(DialogFilter, {
            items: this.statistics,
            onApply: (items) => {
                this.statisticService.setHiddenItems(items.filter(e => e.isHidden).map(e => e.id))
            }
        });
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);

