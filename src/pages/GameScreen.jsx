import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from "../context/AuthContext";
import { getRandomQuestion } from "../api";
import { submitAnswer } from "../api";

// This page is the game container. It displays 4 images or videos which the user may choose from. 
// Runner component is available on this page 

export function GameScreen() {
  // Variables 
  const navigate = useNavigate()
  const [score, setScore] = useState(0)
  const [selected, setSelected] = useState(null)
  const [showFeedback, setShowFeedback] = useState(false)
  const [isAnswered, setIsAnswered] = useState(false)
  const [correctId, setCorrectId] = useState(null)
  const [question, setQuestion] = useState(null);
  const { user, signOut } = useAuth();
  const maxRounds = 5;
  const [questionCount, setQuestionCount] = useState(1);
  console.log("Logged in as:", user?.username);

  useEffect(() => {
    const fetchQuestion = async () => {
      const result = await getRandomQuestion();
      if (result && !result.error){
        // transform backend image paths to match my folder
        const images = result.answers.map((a, index) => ({
          id: a.id,
          url: a.text,  // insert correct image path
          isDeepfake: false, 
      }));

      const correctIndex = Math.floor(Math.random() * images.length);
      images[correctIndex].isDeepfake = true; 
      setQuestion({
        question_id: result.question_id,
        question_text: result.question_text,
        images: images,
      });
    }
  };
    fetchQuestion();
  }, []);

  useEffect(() => {
    if (question) {
      const correct = question.images.find((img) => img.isDeepfake);
      if (correct) setCorrectId(correct.id);
     }
  }, [question]);

  {/* Function to handle user answer selection */}
  const handleAnswer = async (image) => {
    if (isAnswered) return;

    setSelected(image.id);
    setShowFeedback(true);

    let earned = 0;

    if (image.isDeepfake) {
      earned = 10;
      setScore((prev) => prev + earned);
    }

    setIsAnswered(true);

    // Submit to backend
    await submitAnswer({
      user_id: user?.user_id || -1,  //handle guest
      question_id: question.question_id,
      selected_id: image.id,
      correct_id: correctId,
      score_earned: earned,
    });
  };

  {/* Function to go to the next question */}
  const handleNext = () => {
    setSelected(null);
    setShowFeedback(false);
    setIsAnswered(false);
    setCorrectId(null);

    setQuestionCount((prev) => {
      const newCount = prev + 1;
      if(newCount > maxRounds) {
        navigate("/fin", { state: { score } });
      } else{
        setQuestion(null); // Triggers fetching next question
      }
      return newCount;
    });
  };
  
  if (!question) { 
    return <p className="text-white">Loading question...</p>;
  }
  
  return (
    <div className="min-h-screen bg-slate-900 text-white flex flex-col items-center justify-center gap-8 p-4"> {/* Page container */}
      {user?.username ? (
      <p className="text-sm text-slate-400 font-mono">
        Welcome, {user.username}!
      </p>
    ) : (
      <p className="text-sm text-yellow-400 font-mono">
        Playing as guest – your scores won’t be saved.
      </p>
    )}

      <p className="text-sm text-slate-400 font-mono">
        Round {questionCount} / {maxRounds}
      </p>
      <h1 className="text-2xl font-mono">Choose the Deepfake</h1>
      <div className="grid grid-cols-2 gap-4"> {/* Images displayed in a grid */}
        {question.images.map((img) => {
          let borderColor = 'border-transparent'
      
     
      
          {/* Handle correct/incorrect img border coloring*/}
          if (isAnswered) {
            if (img.id === correctId) {
              borderColor = 'border-green-500'
            } else if (img.id === selected) {
              borderColor = 'border-red-500'
            }
          }

          return (
            <button
              key={img.id}
              onClick={() => handleAnswer(img)}
              disabled={isAnswered} // disable so user can't click again
              className={`border-4 rounded-lg overflow-hidden ${borderColor}`}
            >
              <img
                src={img.url}
                alt="choice"
                className="w-40 h-40 object-cover"
              />
            </button>
          )
        })}
      </div>

      {showFeedback && (
        <div className="flex flex-col items-center">
          {/* Pop up text that displays feedback */}
          {selected === correctId ? (
            <p className="text-green-400 text-center font-mono">
              Correct! +10 points
            </p>
          ) : (
            <p className="text-red-400 text-center font-mono">
              Incorrect!
            </p>
          )}

          {/* Continue button */}
          <button
            onClick={handleNext}
            className="mt-4 px-4 py-2 bg-blue-600 rounded hover:bg-blue-500 font-mono"
          >
            Continue
          </button>
        </div>
      )}
    </div>
  )
}
