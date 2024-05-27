/** @odoo-module **/

import { onMounted, useRef } from "@odoo/owl";

export function useAutofocus(ref) {
    const inputRef = useRef(ref);
    onMounted(() => {
        inputRef.el.focus();
    });
}
