import {onMounted, useRef} from "@odoo/owl";

export function useAutoFocus(refName) {
    const myRef = useRef(refName);
    onMounted(() => {
        myRef.el.focus();
    });
}