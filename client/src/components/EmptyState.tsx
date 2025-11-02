import { Button } from "@/components/ui/button";
import { Plus, BookOpen } from "lucide-react";

interface EmptyStateProps {
  onCreateQuestion?: () => void;
}

export default function EmptyState({ onCreateQuestion }: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-16 px-6 text-center">
      <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center mb-4">
        <BookOpen className="h-8 w-8 text-primary" />
      </div>
      <h3 className="text-xl font-semibold mb-2">No questions yet</h3>
      <p className="text-muted-foreground mb-6 max-w-md">
        Get started by creating your first question. Build your educational question bank for quizzes, tests, or practice.
      </p>
      <Button onClick={onCreateQuestion} data-testid="button-create-first">
        <Plus className="h-4 w-4 mr-1.5" />
        Create First Question
      </Button>
    </div>
  );
}
