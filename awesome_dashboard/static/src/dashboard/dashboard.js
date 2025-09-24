/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { Component, useState } from "@odoo/owl";
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
        this.statistics = useService("awesome_dashboard.statistics");
        this.state = useState({items: [], stats: this.statistics});
        this.dialog = useService("dialog");
        this.updateDashboard()
    }

    updateDashboard() {
        let disabledElements = localStorage.getItem('disabledElements') || '';
        if(disabledElements.includes(',')) {
            disabledElements = disabledElements.split(',')
        }
        else{
            disabledElements = [disabledElements]
        }
        this.state.items = registry.category("awesome_dashboard")
            .getAll()
            .filter(el => !disabledElements.some((e) => e == el.id ))
    }

    openCustomers() {
        this.action.doAction('base.action_partner_form')
    }

    openLeads() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: _t('Leads'),
            res_model: 'crm.lead',
            views: [[false, 'list'], [false, 'form']]
        })
    }

    customizeDashboard() {
        let items = []
        let all = registry.category("awesome_dashboard").getAll();
        all.forEach(el => {
            const enabled = this.state.items.some(item => item.id == el.id)
            items.push({
                element: el,
                enabled: enabled
            })
        })

        this.dialog.add(ConfigurationDialog, {
            items: items,
            onApply: this.updateDashboard.bind(this)
        })
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
