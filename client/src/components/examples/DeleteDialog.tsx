import { useState } from 'react';
import { Button } from '@/components/ui/button';
import DeleteDialog from '../DeleteDialog';

export default function DeleteDialogExample() {
  const [open, setOpen] = useState(false);

  return (
    <div className="space-y-4">
      <Button onClick={() => setOpen(true)}>Open Delete Dialog</Button>
      <DeleteDialog
        open={open}
        onOpenChange={setOpen}
        onConfirm={() => {
          console.log('Confirmed delete');
          setOpen(false);
        }}
      />
    </div>
  );
}
