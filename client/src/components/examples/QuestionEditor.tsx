import QuestionEditor from '../QuestionEditor';

export default function QuestionEditorExample() {
  const mockQuestion = {
    id: '1',
    text: 'What is the capital of France?',
    answers: [
      { id: '1', text: 'London', isCorrect: false },
      { id: '2', text: 'Paris', isCorrect: true },
      { id: '3', text: 'Berlin', isCorrect: false },
    ]
  };

  return (
    <QuestionEditor
      question={mockQuestion}
      onSave={(q) => console.log('Save question:', q)}
      onCancel={() => console.log('Cancel edit')}
    />
  );
}
