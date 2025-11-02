import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Plus } from "lucide-react";
import QuestionCard from "@/components/QuestionCard";
import QuestionEditor from "@/components/QuestionEditor";
import SearchBar from "@/components/SearchBar";
import DeleteDialog from "@/components/DeleteDialog";
import EmptyState from "@/components/EmptyState";
import ThemeToggle from "@/components/ThemeToggle";

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

export default function Home() {
  const [view, setView] = useState<'list' | 'create' | 'edit'>('list');
  const [searchQuery, setSearchQuery] = useState('');
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [selectedQuestionId, setSelectedQuestionId] = useState<string | null>(null);
  
  //todo: remove mock functionality
  const [questions, setQuestions] = useState<Question[]>([
    {
      id: '1',
      text: 'What is the capital of France?',
      answers: [
        { id: '1', text: 'London', isCorrect: false },
        { id: '2', text: 'Paris', isCorrect: true },
        { id: '3', text: 'Berlin', isCorrect: false },
        { id: '4', text: 'Madrid', isCorrect: false },
      ]
    },
    {
      id: '2',
      text: 'Which planet is known as the Red Planet?',
      answers: [
        { id: '1', text: 'Venus', isCorrect: false },
        { id: '2', text: 'Mars', isCorrect: true },
        { id: '3', text: 'Jupiter', isCorrect: false },
      ]
    },
    {
      id: '3',
      text: 'What is the largest ocean on Earth?',
      answers: [
        { id: '1', text: 'Atlantic Ocean', isCorrect: false },
        { id: '2', text: 'Indian Ocean', isCorrect: false },
        { id: '3', text: 'Pacific Ocean', isCorrect: true },
        { id: '4', text: 'Arctic Ocean', isCorrect: false },
      ]
    },
  ]);

  const filteredQuestions = questions.filter(q =>
    q.text.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const handleCreateQuestion = (question: { text: string; answers: Answer[] }) => {
    const newQuestion: Question = {
      ...question,
      id: Date.now().toString(),
    };
    setQuestions([newQuestion, ...questions]);
    setView('list');
  };

  const handleEditQuestion = (question: { id?: string; text: string; answers: Answer[] }) => {
    if (question.id) {
      setQuestions(questions.map(q => q.id === question.id ? { ...question, id: question.id } as Question : q));
    }
    setView('list');
    setSelectedQuestionId(null);
  };

  const handleDeleteQuestion = (id: string) => {
    setSelectedQuestionId(id);
    setDeleteDialogOpen(true);
  };

  const confirmDelete = () => {
    if (selectedQuestionId) {
      setQuestions(questions.filter(q => q.id !== selectedQuestionId));
      setSelectedQuestionId(null);
    }
    setDeleteDialogOpen(false);
  };

  const startEdit = (id: string) => {
    setSelectedQuestionId(id);
    setView('edit');
  };

  const selectedQuestion = questions.find(q => q.id === selectedQuestionId);

  return (
    <div className="min-h-screen bg-background">
      <header className="sticky top-0 z-50 border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-primary flex items-center justify-center">
              <span className="text-primary-foreground font-bold text-lg">Q</span>
            </div>
            <h1 className="text-xl font-semibold">QuizMaster</h1>
          </div>
          <ThemeToggle />
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-8">
        {view === 'list' && (
          <div className="space-y-6">
            <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
              <div>
                <h2 className="text-2xl font-semibold">Questions</h2>
                <p className="text-muted-foreground">
                  {questions.length} {questions.length === 1 ? 'question' : 'questions'} in your library
                </p>
              </div>
              <Button onClick={() => setView('create')} data-testid="button-create-question">
                <Plus className="h-4 w-4 mr-1.5" />
                Create Question
              </Button>
            </div>

            {questions.length > 0 && (
              <div className="max-w-2xl">
                <SearchBar
                  value={searchQuery}
                  onChange={setSearchQuery}
                />
              </div>
            )}

            {questions.length === 0 ? (
              <EmptyState onCreateQuestion={() => setView('create')} />
            ) : (
              <div className="grid gap-4">
                {filteredQuestions.length === 0 ? (
                  <div className="text-center py-12">
                    <p className="text-muted-foreground">No questions match your search</p>
                  </div>
                ) : (
                  filteredQuestions.map((question) => (
                    <QuestionCard
                      key={question.id}
                      question={question}
                      onEdit={startEdit}
                      onDelete={handleDeleteQuestion}
                      onClick={startEdit}
                    />
                  ))
                )}
              </div>
            )}
          </div>
        )}

        {view === 'create' && (
          <div className="max-w-3xl mx-auto">
            <QuestionEditor
              onSave={handleCreateQuestion}
              onCancel={() => setView('list')}
            />
          </div>
        )}

        {view === 'edit' && selectedQuestion && (
          <div className="max-w-3xl mx-auto">
            <QuestionEditor
              question={selectedQuestion}
              onSave={handleEditQuestion}
              onCancel={() => {
                setView('list');
                setSelectedQuestionId(null);
              }}
            />
          </div>
        )}
      </main>

      <DeleteDialog
        open={deleteDialogOpen}
        onOpenChange={setDeleteDialogOpen}
        onConfirm={confirmDelete}
      />
    </div>
  );
}
