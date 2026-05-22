import { Component, xml } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { registry } from "@web/core/registry";

export class ConfigDialog extends Component {
    static template = xml`<Dialog title="'Config'" close="close">
    <t t-foreach="items" t-as="item" t-key="item.id">
      <CheckBox id="item.id" value="!props.hiddenItems.includes(item.id)" t-on-change="onChange">
        <t t-out="item.description"/>
      </CheckBox>
    </t>
    <t t-set-slot="footer">
      <button class="btn btn-primary" t-on-click="onClose">
        Update
      </button>
    </t>
  </Dialog>`;
    static components = { Dialog, CheckBox };
    static props = {
        close: Function,
        hiddenItems: Array,
    };

    setup() {
        this.items = registry.category("awesome_dashboard").getAll();
    }

    onChange(event) {
        if (!event.target.checked) {
            this.props.hiddenItems.push(event.target.id);
        } else {
            const itemIndex = this.props.hiddenItems.findIndex((item) => item === event.target.id);
            if (itemIndex !== -1) {
                this.props.hiddenItems.splice(itemIndex, 1);
            }
        }
    }

    onClose() {
        this.props.close();
    }
}
