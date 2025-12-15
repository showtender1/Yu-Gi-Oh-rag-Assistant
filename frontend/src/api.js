export async function askCard(card_name, question) {
  const res = await fetch("http://localhost:8000/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ card_name, question })
  });

  if (!res.ok) {
    throw new Error("서버 요청 실패");
  }

  return res.json();
}
