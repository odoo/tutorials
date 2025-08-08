import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";

export class DashboardDialog extends Component {
    static template = "awesome_dashboard.DashboardDialog";
    static components = { Dialog, CheckBox }
    static props = {
        close: Function,
        updateMetricConfigCallback: Function,
        closeDialog: Function,
        metrics: {
            type: Object,
        },
        metricConfigs: {
            type: Object,
        }
    }

    setup() {
        this.state = useState({
            metricConfigs: this.props.metricConfigs
        })
    }

    applyChanges() {
        this.props.updateMetricConfigCallback(this.state.metricConfigs);
        this.props.close();
    }

    toggleMetricConfig(itemID, checked) {
        this.state.metricConfigs[itemID] = checked;
    }

    closeDialog() {
        this.props.closeDialog();
        this.props.close();
    }
}
