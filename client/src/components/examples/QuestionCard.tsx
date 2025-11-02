import QuestionCard from '../QuestionCard';

export default function QuestionCardExample() {
  const mockQuestion = {
    id: '1',
    text: 'What is the capital of France?',
    answers: [
      { id: '1', text: 'London', isCorrect: false },
      { id: '2', text: 'Paris', isCorrect: true },
      { id: '3', text: 'Berlin', isCorrect: false },
      { id: '4', text: 'Madrid', isCorrect: false },
    ]
  };

  return (
    <QuestionCard
      question={mockQuestion}
      onEdit={(id) => console.log('Edit question:', id)}
      onDelete={(id) => console.log('Delete question:', id)}
      onClick={(id) => console.log('View question:', id)}
    />
  );
}
