/** @odoo-module **/

import { Component, onWillStart, useState, useEffect, reactive } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { rpc } from "@web/core/network/rpc";
import {PieChart} from "./pie_chart/pie_chart"
import { items } from "./dashboard_items";
import { Dialog } from "@web/core/dialog/dialog";
import { DashboardConfigDialog } from "./dailog/Dialog";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = {Layout, DashboardItem, PieChart, Dialog};

    setup(){
        this.action = useService("action");
        this.statisticsService = useState(useService("awesome_dashboard.statistics"));
        this.state = reactive({ statistics: {}, disabledItems: [] });    
        this.items = registry.category("awesome_dashboard").getAll();

        onWillStart(async () => {
            this.state.statistics = await this.statisticsService.loadStatistics();
            this.loadConfig();
        });

        useEffect(() => {
            this.state.statistics = this.statisticsService.statistics.data;
        });
    }

    loadConfig() {
        const config = localStorage.getItem("dashboard_hidden_items");
        this.state.disabledItems = config ? JSON.parse(config) : [];
    }

    openConfiguration() {
        this.env.services.dialog.add(DashboardConfigDialog, {
            items: this.items,
            disabledItems: [...this.state.disabledItems],  
            onSave: (hiddenItems) => {
                localStorage.setItem("dashboard_hidden_items", JSON.stringify(hiddenItems));
                this.state.disabledItems = hiddenItems;  
            },
        });
    }

    openCustomers(){
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            res_model: "crm.lead",
            views: [[false, 'form'], [false, 'list']]
        })
    }
}

registry.category("lazy_components").add("awesome_dashboard.dashboard", AwesomeDashboard);