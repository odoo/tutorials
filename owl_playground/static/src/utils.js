/** @odoo-module **/

import { onMounted, useRef } from "@odoo/owl";

export function useAutofocus(name) {
    const ref = useRef(name);
    onMounted(() => ref.el && ref.el.focus()); //We focus the element when it is mounted
}