/** @odoo-module **/
import { _t } from "@web/core/l10n/translation";
import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks"
import { DashboardItem } from "./components/dashboarditem/dashboarditem";
import { PieChart } from "./components/piechart/piechart";
import { Settings } from "./settings/settings";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PieChart }

    setup(){
        this.action = useService("action")
        this.statistics = useService("awesome_dashboard.statistics")
        this.result = useState(this.statistics.data.stat)
        this.items = registry.category("awesome_dashboard").getAll()
        this.dialog = useService("dialog");
        // get the ids of items to be hidden
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
        // opens the dialog using Settings Component
        this.dialog.add(Settings,{
            onDone : (hiddenItems)=>{
                // update the hidden items based on settings change
                this.hiddenItems.clear();
                hiddenItems.forEach(id => this.hiddenItems.add(id));
            }
        });
    }

    get selectedItems(){
        // return only selected items
        return Object.values(this.items.filter(item => !this.hiddenItems.has(item.id)))
    }
}

registry.category("lazy_components").add("awesome_dashboard.dashboard", AwesomeDashboard);
