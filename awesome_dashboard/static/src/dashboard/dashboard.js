import { Component, useState, xml } from "@odoo/owl";
import { DashboardItem } from "./dashboard_item";
import { Layout } from "@web/search/layout";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Dialog } from "@web/core/dialog/dialog";
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, Dialog, ConfirmationDialog, DashboardDialogBody };

    setup() {
        super.setup();
        this.action = useService("action");
        this.dialogs = useService('dialog');
        this.notification = useService("notification");
        this.statistics = useState(useService("awesome_dashboard.statistics"));
        this.items = registry.category("awesome_dashboard").getAll();
    }

    showKanbanCustomersView() {
        this.action.doAction("base.action_partner_form");
    }

    showLeads() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            res_model: 'crm.lead',
            views: [[false, 'list'], [false, 'form']],
        });
    }

    showSettings() {
        this.dialogs.add(ConfirmationDialog, {
            title: "Dashboard items configuration",
            body: "TODO", // use DashboardDialogBody maybe...
            confirmClass: "btn-primary",
            confirmLabel: "Done",
            confirm: () => {
                                this.notification.add("Changes have been successfully implemented!", {
                                        type: "success",
                                    },
                                );
                            },
        });
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);


export class DashboardDialogBody extends Component {
    static template = xml`
        <div>
            <p><strong>Attention:</strong> cette action est irréversible.</p>
            <p>Voulez-vous vraiment continuer ?</p>
        </div>
    `;
}
