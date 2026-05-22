import { reactive, useState } from "@odoo/owl";

export function useLocalStorage(key, initialState) {
    const state = JSON.parse(localStorage.getItem(key)) || initialState;
    const store = (obj) => localStorage.setItem(key, JSON.stringify(obj));
    const reactiveState = reactive(state, () => store(reactiveState));
    store(reactiveState);
    return useState(state);
}
