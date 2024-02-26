/** @odoo-module **/

import { useRef, onMounted } from "@odoo/owl";

export function useAutoFocus(parent, reference) {
    parent.inputRef = useRef(reference);

    onMounted(() => {
        parent.inputRef.el.focus();
    });
}
