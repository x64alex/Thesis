import CircularProgress from '@mui/material/CircularProgress';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';

function ChatView({
    userInput,
    handleInputChange,
    handleSubmit,
    chatHistory,
    loading,
    chatInputRef
  }) {
    return (
      <>
        <div className="chat-history">
          {chatHistory.map((message, index) => (
            <div key={index}>
              <div>User: {message.user}</div>
              <div>Response: {message.response}</div>
            </div>
          ))}
          <div ref={chatInputRef}></div>
        </div>
        <form className="chat-input" onSubmit={handleSubmit}>
          <TextField 
            type="text" 
            value={userInput} 
            onChange={handleInputChange} 
            label="Enter your message" 
            fullWidth
            disabled={loading}
          />
          <Button 
            type="submit" 
            variant="contained" 
            color="primary" 
            disabled={loading}
          >
            {loading ? <CircularProgress size={24} color="inherit" /> : 'Send'}
          </Button>
        </form>
      </>
    );
  }

  export default ChatView;