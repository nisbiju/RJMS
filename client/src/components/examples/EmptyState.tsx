import EmptyState from '../EmptyState';

export default function EmptyStateExample() {
  return (
    <EmptyState onCreateQuestion={() => console.log('Create first question')} />
  );
}
