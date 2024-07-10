import React, { useState } from 'react';

function App() {
  // 상태 변수를 정의합니다.
  const [message, setMessage] = useState(''); // 사용자가 입력한 메시지
  const [response, setResponse] = useState(''); // 서버에서 받은 응답
  const [error, setError] = useState(''); // 서버에서 받은 에러 메시지
  const [isLoading, setIsLoading] = useState(false); // 로딩 상태

  // 폼 제출 시 호출되는 함수입니다.
  const handleSubmit = async (event) => {
    event.preventDefault();
    setError('');
    setIsLoading(true);
    // 서버에 메시지를 보내기 위한 요청을 보냅니다.
    const res = await fetch(process.env.REACT_APP_API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message }),
    });
    const data = await res.json();
    // 서버에서 받은 응답을 처리합니다.
    if (data.error) {
      setError(data.error);
    } else {
      setResponse(data.response);
    }
    setIsLoading(false);
  };

  return (
    <div className="App">
      <h1>Chatbot</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
        />
        <button type="submit">Send</button>
      </form>
      {error && (
        <div className="error" style={{ color: 'red' }}>
          <h2>Error:</h2>
          <p>{error}</p>
        </div>
      )}
      {isLoading && <p>Loading...</p>}
      <div className="response">
        <h2>Response:</h2>
        <p>{response}</p>
      </div>
    </div>
  );
}

export default App;
