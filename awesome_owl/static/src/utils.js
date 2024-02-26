/** @odoo-module **/

import {onMounted, useRef} from "@odoo/owl";

export function useAutofocus(refName) {
    const ref = useRef(refName);
    onMounted(() => {
        ref.el.focus();
    })
}