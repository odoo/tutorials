import { Component, xml, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { browser } from "@web/core/browser/browser";


export class ConfigurationDialog extends Component {
    static components = { Dialog, CheckBox };
    static template = xml`
        <Dialog>
             <t t-foreach="items" t-as="item" t-key="item.id">
                <CheckBox value="item.enabled" onChange="(ev) => this.onChange(ev, item)">
                    <t t-esc="item.description"/>
                </CheckBox>
            </t>
            <t t-set-slot="footer">
                <button class="btn btn-primary" t-on-click="done">
                    Done
                </button>
            </t>
        </Dialog>
    `;

    static props = {
        items: {Type: Array},
        disabledItems: {Type: Array},
        onUpdateConfiguration: {Type: Function}
    }


    setup() {
        this.items = useState(this.props.items.map((item) => {
            return {
                ...item,
                enabled: !this.props.disabledItems.includes(item.id),
            }
        }));
    }

    onChange(ev, item) {
        item.enabled = ev
        const newDisabledItems = Object.values(this.items).filter(
            (item) => !item.enabled
        ).map((item) => item.id)

        browser.localStorage.setItem(
            "disabledDashboardItems",
            newDisabledItems,
        );

        this.props.onUpdateConfiguration(newDisabledItems);
    }

    done() {
        this.props.close();
    }
}

