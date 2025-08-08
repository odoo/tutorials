/** @odoo-module **/

import { Component, useState, onMounted, onWillUnmount } from '@odoo/owl';
import { registry } from '@web/core/registry';
import { Layout } from '@web/search/layout';
import { useService } from '@web/core/utils/hooks';
import { rpc } from '@web/core/network/rpc';
import { DashboardItem } from './dashboard_item';
import { Dialog } from '@web/core/dialog/dialog';
import { CheckBox } from '@web/core/checkbox/checkbox';
import { browser } from '@web/core/browser/browser';

class AwesomeDashboard extends Component {
    static template = 'awesome_dashboard.AwesomeDashboard';
    static components = { Layout, DashboardItem };

    setup() {
        this.layoutProps = { controlPanel: {} };
        this.action = useService('action');
        this.state = useState({
            statistics: {},
            disabledItems:
                browser.localStorage.getItem('disabledDashboardItems')?.split(',') ||
                [],
        });
        this.dialog = useService('dialog');
        this.items = registry.category('awesome_dashboard').getAll();
        this.fetchData();

        this.intervalId = null;
        onMounted(() => {
            this.intervalId = setInterval(() => {
                this.fetchData();
            }, 1000);
        });

        onWillUnmount(() => {
            if (this.intervalId) {
                clearInterval(this.intervalId);
            }
        });
    }

    async fetchData() {
        const result = await rpc('/awesome_dashboard/statistics', {});
        if (result) {
            this.state.statistics = result;
        }
    }
   
    openConfiguration() {
        this.dialog.add(ConfigurationDialog, {
            items: this.items,
            disabledItems: this.state.disabledItems,
            onUpdateConfiguration: this.updateConfiguration.bind(this),
        });
    }

    updateConfiguration(newDisabledItems) {
        this.state.disabledItems = newDisabledItems;
    }

    openCustomers() {
        this.action.doAction('base.action_partner_form');
    }

    openLeads() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: "Leads",
            res_model: 'crm.lead',
            view_mode: 'kanban,tree,form',
            views: [[false, 'kanban'], [false, 'list'], [false, 'form']],
            target: 'current',
        });
    }
}

class ConfigurationDialog extends Component {
    static template = 'awesome_dashboard.ConfigurationDialog';
    static components = { Dialog, CheckBox };
    static props = ['close', 'items', 'disabledItems', 'onUpdateConfiguration'];

    setup() {
        this.items = useState(
            this.props.items.map((item) => {
                return {
                    ...item,
                    enabled: !this.props.disabledItems.includes(item.id),
                };
            })
        );
    }

    done() {
        this.props.close();
    }

    onChange(checked, changedItem) {
        changedItem.enabled = checked;
        const newDisabledItems = Object.values(this.items)
            .filter((item) => !item.enabled)
            .map((item) => item.id);

        browser.localStorage.setItem('disabledDashboardItem', newDisabledItems);

        this.props.onUpdateConfiguration(newDisabledItems);
    }
}
registry.category('lazy_components').add('AwesomeDashboard', AwesomeDashboard);
