/** @odoo-module **/

import { onMounted, useRef } from "@odoo/owl";


export function useAutofocus(ref) {
    let inputRef = useRef(ref);
    onMounted(() => {
        inputRef.el.focus();
    })
};
