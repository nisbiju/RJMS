import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { CheckCircle2, Edit, Trash2 } from "lucide-react";

interface Answer {
  id: string;
  text: string;
  isCorrect: boolean;
}

interface Question {
  id: string;
  text: string;
  answers: Answer[];
}

interface QuestionCardProps {
  question: Question;
  onEdit?: (id: string) => void;
  onDelete?: (id: string) => void;
  onClick?: (id: string) => void;
}

export default function QuestionCard({ question, onEdit, onDelete, onClick }: QuestionCardProps) {
  const correctAnswerCount = question.answers.filter(a => a.isCorrect).length;
  
  return (
    <Card 
      className="p-6 hover-elevate active-elevate-2 cursor-pointer transition-shadow"
      onClick={() => onClick?.(question.id)}
      data-testid={`card-question-${question.id}`}
    >
      <div className="space-y-4">
        <div className="flex items-start justify-between gap-4">
          <div className="flex-1 min-w-0">
            <h3 className="font-serif text-lg leading-tight line-clamp-2" data-testid="text-question">
              {question.text}
            </h3>
          </div>
          <div className="flex items-center gap-2 flex-shrink-0">
            <Button
              size="icon"
              variant="ghost"
              onClick={(e) => {
                e.stopPropagation();
                onEdit?.(question.id);
              }}
              data-testid="button-edit"
            >
              <Edit className="h-4 w-4" />
            </Button>
            <Button
              size="icon"
              variant="ghost"
              onClick={(e) => {
                e.stopPropagation();
                onDelete?.(question.id);
              }}
              data-testid="button-delete"
            >
              <Trash2 className="h-4 w-4" />
            </Button>
          </div>
        </div>

        <div className="flex items-center gap-3 text-sm text-muted-foreground">
          <div className="flex items-center gap-1.5">
            <Badge variant="secondary" className="text-xs" data-testid="badge-answer-count">
              {question.answers.length} {question.answers.length === 1 ? 'answer' : 'answers'}
            </Badge>
          </div>
          {correctAnswerCount > 0 && (
            <div className="flex items-center gap-1.5 text-green-600 dark:text-green-500">
              <CheckCircle2 className="h-4 w-4" />
              <span className="text-xs font-medium" data-testid="text-correct-count">
                {correctAnswerCount} correct
              </span>
            </div>
          )}
        </div>
      </div>
    </Card>
  );
}
