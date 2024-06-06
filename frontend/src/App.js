import React from 'react';
import ChatContainer from './View/ChatContainer';
import ChatView from './View/ChatView';

import './App.css';


function App() {
  return (
    <ChatContainer
      render={({ userInput, handleInputChange, handleSubmit, chatHistory, loading, chatInputRef }) => (
        <ChatView
          userInput={userInput}
          handleInputChange={handleInputChange}
          handleSubmit={handleSubmit}
          chatHistory={chatHistory}
          loading={loading}
          chatInputRef={chatInputRef}
        />
      )}
    />
  );
}

export default App;
