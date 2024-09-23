/** @odoo-module **/

import {onMounted, useRef} from "@odoo/owl";

export function useAutoFocus(refName) {
    const ref = useRef(refName);
    onMounted(() => {
        ref.el.focus();
    });
}