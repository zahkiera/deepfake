import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'

const dummyData = [
  {
    id: 1,
    images: [
      { id: 'a', url: '/images/img1.jpg', isDeepfake: false },
      { id: 'b', url: '/images/img2.jpg', isDeepfake: true }, // correct answer
      { id: 'c', url: '/images/img3.jpg', isDeepfake: false },
      { id: 'd', url: '/images/img4.jpg', isDeepfake: false },
    ],
  },
]

{/* This page is the game container. It displays 4 images or videos which the user may choose from.  */}
{/* Runner component is available on this page */}

export function GameScreen() {
  {/* Variables */}
  const navigate = useNavigate()
  const [questionIndex, setQuestionIndex] = useState(0)
  const [score, setScore] = useState(0)
  const [selected, setSelected] = useState(null)
  const [showFeedback, setShowFeedback] = useState(false)
  const [isAnswered, setIsAnswered] = useState(false)
  const [correctId, setCorrectId] = useState(null)

  const currentQuestion = dummyData[questionIndex]

  useEffect(() => {
    const correct = currentQuestion.images.find((img) => img.isDeepfake)
    if (correct) setCorrectId(correct.id)
  }, [currentQuestion])

  {/* Function to handle user answer selection */}
  const handleAnswer = (image) => {
    if (isAnswered) return

    setSelected(image.id)
    setShowFeedback(true)

    if (image.isDeepfake) {
      setScore((prev) => prev + 10)
    }

    setIsAnswered(true)
  }

  {/* Function to go to the next question */}
  const handleNext = () => {
    setSelected(null)
    setShowFeedback(false)
    setIsAnswered(false)

    if (questionIndex < dummyData.length - 1) {
      setQuestionIndex((prev) => prev + 1)
    } else {
      navigate('/fin', { state: { score } }) // navigate and pass final score to game finish page
    }
  }

  return (
    <div className="min-h-screen bg-slate-900 text-white flex flex-col items-center justify-center gap-8 p-4"> {/* Page container */}
      <h1 className="text-2xl font-mono">Choose the Deepfake</h1>
      <div className="grid grid-cols-2 gap-4"> {/* Images displayed in a grid */}
        {currentQuestion.images.map((img) => {
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
