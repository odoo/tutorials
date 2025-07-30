import { Component, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { Dialog } from "@web/core/dialog/dialog";

export class DashboardDialog extends Component {
    static template = "awesome_dashboard.DashboardDialog";
    static props = {
        close: Function,
        items: {
            type: Object,
        }
    }
    static components = { Dialog }
    setup() {
        this.statisticsService = useService("awesome_dashboard.statistics");
        this.itemsState = useState(this.statisticsService.itemsState);
    }

    _confirm() {
        const checkboxes = document.getElementsByClassName("form-check-input");
        const removedIds = Array.from(checkboxes).reduce((acc, checkbox) => {
            if (!checkbox.checked) {
                acc.push(checkbox.dataset.id);
            }
            return acc;
        }, []);
        this.itemsState.removedIds = removedIds;
        this.props.close();
    }
}
