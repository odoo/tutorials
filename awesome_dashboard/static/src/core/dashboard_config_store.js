/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { Reactive } from "@web/core/utils/reactive";


class DashboardConfigStore extends Reactive {
    static serviceDependencies = ['bus_service', 'orm', 'user'];
    _disabledItemsState = undefined;

    constructor() {
        super();
        this.setup(...arguments);
    }

    setup(env, { bus_service, orm, user }) {
        this.busService = bus_service;
        this.orm = orm;
        this.userService = user;
    }

    get disabledItems() {
        if (typeof this._disabledItemsState === 'undefined') {
            this._initializeDisabledItems();
        }

        return this._disabledItemsState;
    }

    set disabledItems(value) {
        this._disabledItemsState.splice(0);
        this._disabledItemsState.push(...value);
    }

    async save() {
        await this.userService.setUserSettings('dashboard_settings', JSON.stringify(this.disabledItems));
    }

    setItem(id, targetIsVisible) {
        const index = this.disabledItems.indexOf(id);
        const currentIsDisabled = index >= 0;
        if (targetIsVisible && currentIsDisabled) {
            this.disabledItems.splice(index, 1);
        } else if (!targetIsVisible && !currentIsDisabled) {
            this.disabledItems.push(id);
        }
    }

    _initializeDisabledItems() {
        this._disabledItemsState = [];
        this._tryLoadDisabledItemsFromJson(this.userService.settings.dashboard_settings);

        this.busService.subscribe("res.users.settings", (payload) => {
            if (payload) {
                this._tryLoadDisabledItemsFromJson(payload.dashboard_settings);
            }
        });
    }

    _tryLoadDisabledItemsFromJson(rawJson) {
        if (!rawJson) {
            this.disabledItems = [];
            return;
        }

        let parsedData;
        try {
            parsedData = JSON.parse(rawJson);
        } catch (e) {
            if (e instanceof SyntaxError) {
                const error = new Error(_t("Couldn't parse dashboard settings."));
                error.cause = e;
                throw error;
            } else {
                throw e;
            }
        }
        this.disabledItems = parsedData;
    }
}

const dashboardService = {
    dependencies: DashboardConfigStore.serviceDependencies,
    start(env, dependencies) {
        return new DashboardConfigStore(env, dependencies);
    }
};

registry.category("services").add("awesome_dashboard.dashboard_config", dashboardService);
