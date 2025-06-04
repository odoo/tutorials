/** @odoo-module **/

import { onMounted, useRef } from "@odoo/owl";

export function useAutoFocus(refname) {
    const inputRef = useRef(refname)

    onMounted(() => {
       if (inputRef.el) {
            inputRef.el.focus();
        }
    });
}