import { Component } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";
import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";
import { registry } from "@web/core/registry";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
     static components = {
        Layout
     };

     setup() {
        this.display = {
            controlPanel: {},
        };
        this.action = useService("action");
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
