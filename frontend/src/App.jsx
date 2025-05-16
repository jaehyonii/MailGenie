import { useState } from "react";

function App() {
  const [situation, setSituation] = useState("");
  const [sender, setSender] = useState("");
  const [reciever, setReciever] = useState("");
  const [emailDraft, setEmailDraft] = useState("");
  const [loading, setLoading] = useState(false);

  const generateDraft = async () => {
    setLoading(true);
    setEmailDraft("");

    try {
      const params = new URLSearchParams({
        situation: situation,
        sender: sender,
        reciever: reciever,
      });

      //const response = await fetch(`http://localhost:8000/gen-mail-form?${params}`); // 실제로 쓰는 것
      const response = await fetch(`http://localhost:8000/hello`); // 실험용
      console.log("fetch completed",  response);
      const data = await response.text();
      console.log("response.text() completed", data);
      setEmailDraft(data || "결과 없음");
    } catch (err) {
      setEmailDraft("에러 발생: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 600, margin: "auto", padding: 20 }}>
      <h2>메일 초안 생성기</h2>
      <input
        type="text"
        placeholder="상황 설명"
        value={situation}
        onChange={(e) => setSituation(e.target.value)}
        style={{ width: "100%", marginBottom: 10 }}
      />
      <input
        type="text"
        placeholder="보내는 사람"
        value={sender}
        onChange={(e) => setSender(e.target.value)}
        style={{ width: "100%", marginBottom: 10 }}
      />
      <input
        type="text"
        placeholder="받는 사람"
        value={reciever}
        onChange={(e) => setReciever(e.target.value)}
        style={{ width: "100%", marginBottom: 10 }}
      />
      <button onClick={generateDraft} disabled={loading}>
        {loading ? "생성 중..." : "메일 초안 생성"}
      </button>
      {emailDraft && (
        <div style={{ marginTop: 20, whiteSpace: "pre-wrap", background: "#f0f0f0", padding: 10 }}>
          <h3>📩 생성된 메일:</h3>
          <div style={{ whiteSpace: "pre-wrap" }}>
            {emailDraft}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
