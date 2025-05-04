async function getTaxInfo() {
  const state = document.getElementById("state").value;
  const income = document.getElementById("income").value;

  const response = await fetch("http://127.0.0.1:5000/tax-query", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ state, income })
  });

  const data = await response.json();
  document.getElementById("result").innerText = data.result;
}
