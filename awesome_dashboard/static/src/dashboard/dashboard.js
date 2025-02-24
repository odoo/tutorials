/** @odoo-module **/

import { Component, onWillStart, useState, useEffect } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import { DashboardItem } from "./dashboard_item";
import { Piechart } from "../piechart";
import { NumberCard } from "./number_card";
import { PieChartCard } from "./piechart_card";
import { items } from "./dashboard_items";
class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components={Layout, DashboardItem, Piechart, NumberCard, PieChartCard}
    setup(){
        this.action= useService("action");
        this.statisticsService= useService('awesome_dashboard.statistics');
        this.items =registry.category("awesome_dashboard.items").getAll();
        this.result= useState(this.statisticsService.data)
        this.chartData = useState({ labels: [], data: [] });
        this.chartData = {
            labels: [],
            data: []
        };
        useEffect(() => {
            this.chartData.labels = Object.keys(this.result.orders_by_size);
            this.chartData.data = Object.values(this.result.orders_by_size);
            console.log("Updated chartData", this.chartData);
        });
        onWillStart(async () => {
            try {
                // const data = await this.statisticsService.loadStatistics();
                // this.result=data;
                this.chartData.labels = Object.keys(this.result.orders_by_size);
                this.chartData.data = Object.values(this.result.orders_by_size);
                console.log(this.result)
            } catch (error) {
                console.error("Failed to fetch statistics:", error);
            }
        });
    }

    customers_kanban_view(){
        this.action.doAction("base.action_partner_form")
    }

    open_leads(){
        this.action.doAction({
            type:'ir.actions.act_window',
            name:_t('Leads'),
            target:'current',
            res_model:'crm.lead',
            views:[[false, 'list'], [false, 'form']]
        })
    }
}

registry.category("lazy_components").add("awesome_dashboard.dashboard", AwesomeDashboard);
