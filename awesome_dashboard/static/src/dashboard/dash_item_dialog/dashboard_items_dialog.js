import { Dialog } from "@web/core/dialog/dialog";
import { Component } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class DashboardItemDialog extends Component {
    static template = "awesome_dashboard.dashboard_items_dialog";
    static components = {
        Dialog,
    };

    setup() {
        this.service = useService("dashboard_items");
        this.allItems = this.service.getAllItems();
        this.usedIds = this.service.getUsedIds();
    }

    isSelected(id) {
        return this.usedIds.includes(id);
    }

    select(id) {
        return () => {
            let found = this.usedIds.indexOf(id);
            if(found >= 0) this.usedIds.splice(found, 1);
            else this.usedIds.push(id);
        }
    }

    apply() {
        this.service.setUsedIds(this.usedIds);
        this.props?.close()
    }
}
