import React, { useState } from "react";
import { askCard } from "../api";

export default function AskCard() {
  const [card, setCard] = useState("");
  const [q, setQ] = useState("");
  const [ans, setAns] = useState("");

  const ask = async () => {
    const data = await askCard(card, q);
    setAns(data.answer);
  };

  return (
    <div>
      <input placeholder="카드명" onChange={e=>setCard(e.target.value)} />
      <input placeholder="질문" onChange={e=>setQ(e.target.value)} />
      <button onClick={ask}>질문</button>
      <p>{ans}</p>
    </div>
  );
}
