/** @odoo-module */

export const CURRENT_VERSION = 1.0;
export const migrations = [];

export function migrate(localState) {
  if (localState?.version === CURRENT_VERSION) return;

  for (const migration of migrations) {
    if (localState.version !== migration.fromVersion) continue;

    migration.apply(localState);
    localState.version = migration.toVersion;
  }
  localState.version = CURRENT_VERSION;

  return localState;
}
