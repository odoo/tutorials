/** @odoo-module **/

let scannedProductIds = new Set();

export function getScannedProducts() {
    const stored = localStorage.getItem('scannedProductIds');
    return stored ? new Set(JSON.parse(stored)) : new Set();
}

export function saveScannedProducts(ids) {
    localStorage.setItem('scannedProductIds', JSON.stringify(Array.from(ids)));
}

export function clearScannedProducts() {
    scannedProductIds.clear();
    localStorage.removeItem('scannedProductIds');
}

scannedProductIds = getScannedProducts();

export function addScannedProduct(productId) {
    scannedProductIds.add(productId);
    saveScannedProducts(scannedProductIds);
}