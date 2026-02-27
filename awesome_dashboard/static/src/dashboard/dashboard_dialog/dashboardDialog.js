import { Component } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";
import { useChildRef } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";
import { Dialog } from "@web/core/dialog/dialog";

export class DashboardDialog extends Component {
    static template = "awesome_dashboard.DashboardDialog"
    static components = {
        Dialog
    }
    static props = {
        hidden: {type: Array, element: String},
        save: Function,
        close: Function
    }

    setup(){
        this.disabled = this.props.hidden;
        //this.disabled = JSON.parse(localStorage.getItem("awesome_dashboard/hidden_items")) || [];

        this.items = registry.category("awesome_dashboard").getAll();

        this.size = "lg";
        this.title = _t("Dashboard Items Configuration");
        this.modalRef = useChildRef();
    }

    changeChoices(event){
        const id = event.target.attributes.tag.nodeValue;
        const value = event.target.checked;

        this.disabled = this.disabled.filter((val) => val !== id);
        
        if (!value) {
            this.disabled.push(id);
        }
    }

    close(){
        this.props.save(this.disabled);
        //localStorage.setItem("awesome_dashboard/hidden_items", JSON.stringify(this.disabled));
        this.props.close();
    }
}