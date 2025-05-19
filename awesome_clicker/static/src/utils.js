import { useState } from '@odoo/owl';
import { useService } from '@web/core/utils/hooks';

export function useClicker() {
    return useState(useService('awesome_clicker.clicker'));
}

export function choose(array, condition = () => true) {
    // note: this method might not generate a uniform distribution
    let index = Math.floor(array.length * Math.random());
    let tries = 0;
    while (tries < array.length) {
        if (condition(array[index])) {
            return array[index];
        }
        index = (index + 1) % array.length;
        tries++;
    }
    return null;
}

export function isValidNum(num) {
    return typeof num === 'number' && !isNaN(num) && isFinite(num);
}

export function getValidNum(num, def = 0) {
    if (isValidNum(num)) {
        return num;
    }
    return def;
}

export function findMigrationPath(migrations, from, to) {
    if (from == to) {
        return [];
    }
    for (const migration of migrations) {
        if (migration.fromVersion == from) {
            const path = findMigrationPath(migrations, migration.toVersion, to);
            if (path) {
                return [migration, ...path];
            }
        }
    }
    return null;
}
