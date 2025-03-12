/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { _t } from "@web/core/l10n/translation";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./components/dashboarditem/dashboarditem";
import { Settings } from "./settings/settings";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem }

    setup(){
        this.statistic_service = useService("awesome_dashboard.statistics");
        this.result = useState({data: null});
        this.action = useService("action");
        this.result.data = this.statistic_service.stats;
        this.items = registry.category("awesome_dashboard").getAll();
        this.state = useState({ showDialog: false });
        this.dialog = useService("dialog");
        const storedHiddenItems = JSON.parse(localStorage.getItem('hiddenDashboardItems')) || []
        this.hiddenItems = useState(new Set(storedHiddenItems))
    }

    opoenCustomers(){
        this.action.doAction("base.action_partner_form")
    }

    openLeads(){
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: _t('Leads'),
            target: 'current',
            res_model: 'crm.lead',
            views: [[false,'list'],[false,'form']]
        })
    }

    openSettings(){
        this.dialog.add(Settings,{
            onDone : (hiddenItems)=>{
                this.hiddenItems.clear();
                hiddenItems.forEach(id => this.hiddenItems.add(id));
            }
        });
    }

    get selectedItems(){
        return Object.values(this.items.filter(item => !this.hiddenItems.has(item.id)))
    }
}

registry.category("lazy_components").add("awesome_dashboard.dashboard", AwesomeDashboard);
