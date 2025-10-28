/** @odoo-module **/

import { useRef, onMounted } from '@odoo/owl'

export function useAutoFocus(name) {
    const inputRef = useRef(name);
    onMounted(() => {
        inputRef.el.focus();
    })
}
