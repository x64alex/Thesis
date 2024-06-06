## Run backend with:
flask --app backend.py run  


## Design Patterns in project

### 1. Singleton Pattern - Creational - Sentiment Analysis

#### Implementation(constants.py):

```python
class Constants(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Constants, cls).__new__(cls)
            cls.instance._constants = {}
        return cls.instance

    def set_constant(self, key, value):
        self._constants[key] = value

    def get_constant(self, key):
        return self._constants.get(key)

### 2. Strategy Pattern - Behavioral - JCML

#### Implementation(interpret.py):

```python
class MatchingStrategy(ABC):
    @abstractmethod
    def match_pattern(self, input_text, pattern, types):
        pass


class JCMLMatchingStrategy(MatchingStrategy):
    def match_pattern(self, input_text, pattern, types):
        ...

class JCML:
    def __init__(self, filename, matching_strategy = JCMLMatchingStrategy()):
        ...
        self.matching_strategy = matching_strategy

### 3. Adapter Pattern - Structural - Sentiment Analysis
#### Implementation(SocialClient.py):
```python
class RedditAdapter:
    def __init__(self, client_id = None, client_secret = None, user_agent = None):
        ...

    def get_hot_posts(self, input, limit=10):
        return self.comunicator.subreddit(input).hot(limit=limit)

class AbstractSocialClient(ABC):
    def __init__(self, adapter, text_cleaner=None):
        self.adapter = adapter
        if text_cleaner is None:
            self.text_cleaner = TextCleaner()
        else:
            self.text_cleaner = text_cleaner

    @abstractmethod
    def get_posts(self, input, count=10):
        pass
 
### 4. Strategy Pattern - Structural - Sentiment Analysis
#### Implementation(SocialClient.py):
```python
class TextCleaner:
    def clean_text(self, text):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", text).split())

### 5. Prototype Pattern - Creational - Sentiment Analysis
#### Implementation(SocialClient.py):
```python
class SocialClient(AbstractSocialClient):
    def get_posts(self, input, count=10):
        posts = []
        for submission in self.adapter.get_hot_posts(input, limit=count):
            clean_title = self.text_cleaner.clean_text(submission.title)
            posts.append(clean_title)
        return posts

### 6. Render Props - React patterns - Frontend
[Link to Article](https://www.patterns.dev/react/render-props-pattern/)
#### Implementation(View folder):


```javascript
function ChatContainer({ render }) {
    ...
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
        ...
    );
  }
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

