/** @odoo-module **/

import { onMounted, useRef } from "@odoo/owl";

export function useAutofocus(tagTRef) {
    const tagRef = useRef(tagTRef)
    onMounted(() => {
        tagRef.el.focus()
    });
}
