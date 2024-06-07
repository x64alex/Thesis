import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';


function ChatContainer({ render }) {
  const [userInput, setUserInput] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const chatInputRef = useRef(null);

  useEffect(() => {
    chatInputRef.current.scrollIntoView({ behavior: 'smooth' });
  }, [chatHistory]);

  const handleInputChange = (e) => {
    setUserInput(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/get_response', {
      // const response = await axios.post('https://api-b2b2vg7pfa-uc.a.run.app/get_response', {
        user_input: userInput
      });
      setLoading(false);
      const newMessage = { user: userInput, response: response.data.response };
      setChatHistory([...chatHistory, newMessage]);
      setUserInput('');
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className="app-container">
      {render({
        userInput,
        handleInputChange,
        handleSubmit,
        chatHistory,
        loading,
        chatInputRef
      })}
    </div>
  );
}

export default ChatContainer;