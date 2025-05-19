import { Component } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { useChildRef } from "@web/core/utils/hooks";

export class ConfigDialog extends Component {
    static template = "awesome_dashboard.config_dialog";
    static components = { Dialog };
    static props = {
        title: String,
        description: String,
        items: {
            type: Array,
            element: { type: Object, shape: { id: String, enabled: Boolean, label: String } }
        },
        confirm: Function,
    };

    setup() {
        this.modalRef = useChildRef();
        this.states = {};

        this.props.items.forEach((item) => this.states[item.id] = item.enabled);
    }

    async _confirm() {
        return this.execButton(this.props.confirm);
    }

    setButtonsDisabled(disabled) {
        this.isProcess = disabled;
        if (!this.modalRef.el) {
            return; // safety belt for stable versions
        }
        for (const button of [...this.modalRef.el.querySelectorAll(".modal-footer button")]) {
            button.disabled = disabled;
        }
    }

    async execButton(callback) {
        if (this.isProcess) {
            return;
        }
        this.setButtonsDisabled(true);
        if (callback) {
            let shouldClose;
            try {
                shouldClose = await callback(this.states);
            } catch (e) {
                this.props.close();
                throw e;
            }
            if (shouldClose === false) {
                this.setButtonsDisabled(false);
                return;
            }
        }
        this.props.close();
    }

    onChange(event) {
        this.states[event.target.id] = event.target.checked;
    }
}
