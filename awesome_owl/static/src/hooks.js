/** @odoo-module **/

import { reactive, useState } from "@odoo/owl";

export function useStoredState(key, initialState) {
    const saved = JSON.parse(localStorage.getItem(key)) || initialState;

    const store = (obj) => {
        localStorage.setItem(key, JSON.stringify(obj));
    };

    const reactiveState = reactive(saved, () => store(reactiveState));
    store(reactiveState);

    return useState(saved);
}
