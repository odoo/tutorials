/**
 * useAutofocus - helper to focus an input element
 * @param {Component} component - the component instance
 * @param {string} refName - the t-ref name of the input element
 */
export function useAutofocus(component, refName) {
    // Store original mounted method
    const originalMounted = component.mounted;

    component.mounted = function () {
        // Call original mounted() if it exists
        if (originalMounted) {
            originalMounted.call(this);
        }

        // Focus the element
        if (this.refs && this.refs[refName]) {
            this.refs[refName].focus();
        }
    };
}
