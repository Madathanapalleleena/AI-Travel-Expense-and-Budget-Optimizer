document.getElementById("promptForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const prompt = document.getElementById("prompt").value.trim();
  const resultBox = document.getElementById("result");
  const categoryBox = document.getElementById("categoryBox");

  resultBox.textContent = "Generating response...";
  categoryBox.textContent = "--";

  try {
    const res = await fetch("http://127.0.0.1:5000/agent", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt })
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.error || `Request failed (${res.status})`);
    }

    const data = await res.json();

    categoryBox.textContent = data.category || "Unknown";

    resultBox.textContent = data.response || "No response returned.";
  } catch (err) {
    console.error(err);
    resultBox.textContent = "" + err.message;
  }
});