import { Component, useExternalListener } from '@odoo/owl';
import { registry } from '@web/core/registry';
import { useService } from '@web/core/utils/hooks';
import { useClicker } from './utils';
import { ClickValue } from './click_value';
import { Dropdown } from '@web/core/dropdown/dropdown';
import { DropdownItem } from '@web/core/dropdown/dropdown_item';
import { clickerCommands } from './clicker_commands';

class ClickerSystrayItem extends Component {
    static template = 'awesome_clicker.ClickerSystrayItem';
    static components = { ClickValue, Dropdown, DropdownItem };

    setup() {
        this.clicker = useClicker();
        this.action = useService('action');
        this.commands = [];
        for (const command of clickerCommands) {
            const services = [];
            for (const serviceName of command.services) {
                services.push(useService(serviceName));
            }
            const action = () => command.action(services);
            this.commands.push({
                name: command.name,
                action
            });
        }
        useExternalListener(window, 'click', () => this.clicker.increment(1), { capture: true });
    }

    open() {
        this.action.doAction({
            type: 'ir.actions.client',
            tag: 'awesome_clicker.client_action',
            target: 'new',
            name: 'Clicker',
        });
    }
};

registry.category("systray").add(
    'awesome_clicker.ClickerSystrayItem',
    { Component: ClickerSystrayItem },
    { sequence: 999 }
);
