/** @odoo-module **/

import { useRef, useEffect } from '@odoo/owl';

export function useAutoFocus() {
    const elemRef = useRef("elem");

    useEffect(() => {
        elemRef.el && elemRef.el.focus()
    }, () => []);

    return elemRef;
}
