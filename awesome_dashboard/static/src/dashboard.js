import {Component, onWillStart, useState} from "@odoo/owl";
import {_t} from "@web/core/l10n/translation";
import {useService} from "@web/core/utils/hooks";
import {Layout} from "@web/search/layout";
import {registry} from "@web/core/registry";
import {DashboardItem} from "./dashboard_item/dashboard_item"

class AwesomeDashboard extends Component {
     static template = "awesome_dashboard.AwesomeDashboard";
     static components = { Layout, DashboardItem };

     setup() {
        this.display = {
            controlPanel: {},
        };
        this.action = useService("action");

        this.dashStatsService = useService("awesome_dashboard.statistics");

        onWillStart(async () => {
            this.stats = await this.dashStatsService.loadStatistics();
        })

    }

    openCustomers() {
         this.action.doAction("base.action_partner_form", {
             viewType: "kanban"
         });
    }

    openLeads() {
         this.action.doAction({
            type: 'ir.actions.act_window',
            name: _t('Leads'),
            target: 'new',
            res_model: "crm.lead",
            views: [
                [false, "list"],
                [false, "form"]
            ],
        });
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
