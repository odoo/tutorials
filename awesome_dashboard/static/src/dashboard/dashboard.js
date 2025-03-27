/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from '@web/search/layout';
import { useBus, useService } from '@web/core/utils/hooks';
import { _t } from "@web/core/l10n/translation";
import { DashboardItem } from "./dashboarditem/dashboard_item";
import { PieChart } from "./piechart/pie_chart";
import { SettingDialog } from "./settingdialog/setting_dialog";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PieChart, SettingDialog }

    setup(){
        this.dialogService = useService("dialog");
        this.action = useService("action");
        const statisticsService = useService("awesome_dashboard.statistics");
        this.statistics = useState(statisticsService.statistics);
        this.state = useState({ items: [] });

        // onWillStart(async () => {
        //     const result = await this.statisticsService.loadStatistics();
        //     Object.assign(this.statistics, result);
        //     console.log(result);

        // });

        useBus(this.env.bus, "dashboard_settings_updated", async () => {
            await this.getItems();
        });

        this.getItems()

    }
    async getItems(){
        // this.state.items = []
        const uncheckedItems = JSON.parse(localStorage.getItem("unchecked_dashboard_items")) || [];
        const dashboardRegistry = registry.category("awesome_dashboard");
        this.state.items = Object.values(dashboardRegistry.getAll())
            .filter(item => !uncheckedItems.includes(item.id));
    }

    openCustomersKanban(){
        this.action.doAction("base.action_partner_form");
    }

    async openCrmLead(crm){
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: _t('CRM Lead'),
            target: 'current',
            res_model: 'crm.lead',
            views: [[false, 'list'],[false, 'form']],
        });
    }

    openSettings() {
        this.dialogService.add(SettingDialog);
    }

}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
