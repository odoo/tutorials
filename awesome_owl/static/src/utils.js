import { useRef, onMounted } from "@odoo/owl";

export function useAutoFocus(refName) {
    const fieldRef = useRef(refName);
    onMounted(() => { fieldRef.el.focus(); });
    return fieldRef;
}
