import { setupPullCard } from './pullShared';

setupPullCard({
  key: 'tracked_objects',
  buttonId: 'btn-pull-objects',
  statusId: 'status-objects',
  treeId: 'tree-objects',
  pullPath: '/api/objects',
  loadDataPath: '/api/objects',
});
