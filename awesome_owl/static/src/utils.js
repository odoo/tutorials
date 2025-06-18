import { onMounted, useRef } from "@odoo/owl";

export function useAutofocus(ref_name) {
    const inputRef = useRef(ref_name);

    onMounted(() => {
        inputRef.el.focus();
    });
}
