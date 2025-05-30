import {useRef, onMounted} from "@odoo/owl";


export function useAutoFocus(name) {
    const ref = useRef(name);
    onMounted(() => {
        ref.el.focus();
    });
}
