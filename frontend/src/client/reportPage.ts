import { setupPullCard } from './pullShared';

setupPullCard({
  key: 'orbital_snapshots',
  buttonId: 'btn-pull-snapshots',
  statusId: 'status-snapshots',
  treeId: 'tree-snapshots',
  pullPath: '/api/snapshot',
  loadDataPath: '/api/snapshot/dates',
});
