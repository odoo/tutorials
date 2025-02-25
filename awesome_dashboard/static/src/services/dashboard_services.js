/** @odoo-module */

import { registry } from '@web/core/registry';

const helloService = {
    dependencies: ['notification'],
    start(env, { notification }) {
        return {
            getNotification() {
                notification.add("Hello! This is a notification.");
            },
        };
    },
};
registry.category('services').add('hello_service', helloService);
