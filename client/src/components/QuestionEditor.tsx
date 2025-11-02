import { useState } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Plus, X, GripVertical } from "lucide-react";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";

interface Answer {
  id: string;
  text: string;
  isCorrect: boolean;
}

interface Question {
  id?: string;
  text: string;
  answers: Answer[];
}

interface QuestionEditorProps {
  question?: Question;
  onSave?: (question: Question) => void;
  onCancel?: () => void;
}

export default function QuestionEditor({ question, onSave, onCancel }: QuestionEditorProps) {
  const [questionText, setQuestionText] = useState(question?.text || '');
  const [answers, setAnswers] = useState<Answer[]>(
    question?.answers || [
      { id: '1', text: '', isCorrect: false },
      { id: '2', text: '', isCorrect: false },
    ]
  );

  const addAnswer = () => {
    const newAnswer: Answer = {
      id: Date.now().toString(),
      text: '',
      isCorrect: false,
    };
    setAnswers([...answers, newAnswer]);
  };

  const removeAnswer = (id: string) => {
    if (answers.length > 2) {
      setAnswers(answers.filter(a => a.id !== id));
    }
  };

  const updateAnswerText = (id: string, text: string) => {
    setAnswers(answers.map(a => a.id === id ? { ...a, text } : a));
  };

  const setCorrectAnswer = (id: string) => {
    setAnswers(answers.map(a => ({ ...a, isCorrect: a.id === id })));
  };

  const handleSave = () => {
    onSave?.({
      id: question?.id,
      text: questionText,
      answers: answers.filter(a => a.text.trim() !== ''),
    });
  };

  const correctAnswerId = answers.find(a => a.isCorrect)?.id || '';

  return (
    <Card className="p-8">
      <div className="space-y-6">
        <div>
          <h2 className="text-2xl font-semibold mb-6">
            {question?.id ? 'Edit Question' : 'Create New Question'}
          </h2>
        </div>

        <div className="space-y-2">
          <Label htmlFor="question-text">Question</Label>
          <Textarea
            id="question-text"
            placeholder="Enter your question here..."
            value={questionText}
            onChange={(e) => setQuestionText(e.target.value)}
            className="min-h-24 font-serif text-lg resize-none"
            data-testid="input-question"
          />
        </div>

        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <Label>Answer Options</Label>
            <Button
              type="button"
              variant="outline"
              size="sm"
              onClick={addAnswer}
              data-testid="button-add-answer"
            >
              <Plus className="h-4 w-4 mr-1.5" />
              Add Answer
            </Button>
          </div>

          <RadioGroup value={correctAnswerId} onValueChange={setCorrectAnswer}>
            <div className="space-y-3">
              {answers.map((answer, index) => (
                <div
                  key={answer.id}
                  className="flex items-start gap-3 p-4 rounded-lg border bg-card hover-elevate"
                  data-testid={`answer-option-${index}`}
                >
                  <div className="flex items-center gap-3 flex-1">
                    <GripVertical className="h-4 w-4 text-muted-foreground flex-shrink-0" />
                    <RadioGroupItem
                      value={answer.id}
                      id={`answer-${answer.id}`}
                      className="flex-shrink-0"
                      data-testid={`radio-correct-${index}`}
                    />
                    <Input
                      placeholder={`Answer option ${index + 1}`}
                      value={answer.text}
                      onChange={(e) => updateAnswerText(answer.id, e.target.value)}
                      className="flex-1"
                      data-testid={`input-answer-${index}`}
                    />
                  </div>
                  {answers.length > 2 && (
                    <Button
                      type="button"
                      variant="ghost"
                      size="icon"
                      onClick={() => removeAnswer(answer.id)}
                      data-testid={`button-remove-answer-${index}`}
                    >
                      <X className="h-4 w-4" />
                    </Button>
                  )}
                </div>
              ))}
            </div>
          </RadioGroup>

          <p className="text-sm text-muted-foreground">
            Select the radio button to mark the correct answer
          </p>
        </div>

        <div className="flex items-center gap-3 pt-4">
          <Button onClick={handleSave} data-testid="button-save">
            {question?.id ? 'Update Question' : 'Create Question'}
          </Button>
          <Button variant="outline" onClick={onCancel} data-testid="button-cancel">
            Cancel
          </Button>
        </div>
      </div>
    </Card>
  );
}
