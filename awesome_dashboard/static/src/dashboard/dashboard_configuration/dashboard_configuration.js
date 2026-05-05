import { Component, useRef, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { _t } from "@web/core/l10n/translation";

export class DashboardConfiguration extends Component {
    static template = "awesome_dashboard.DashboardConfiguration";
    static components = {Dialog, CheckBox, _t};
    static props = ["close", "items", "disabledItems", "doneUpdating"];


    setup() {
        this.options = useRef("options");
        this.items = useState(this.props.items.map(item => ({...item, disabled: this.props.disabledItems.includes(item.id)})));
        this.title = _t('Dashboard items configuration');
    }

    updateDisabled(item, checked) {
        item.disabled = !checked;
    }

    apply() {
        const disabledItems = this.items.filter(item => item.disabled).map(item => item.id);
        localStorage.setItem("awesome_dashboard_disabled", disabledItems);
        this.props.doneUpdating(disabledItems);
        this.props.close();
    }
}
