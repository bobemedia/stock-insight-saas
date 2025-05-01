const apiBase = "https://your-backend-url.onrender.com"; // replace after deploy

document.getElementById("scanForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const data = new FormData(e.target);
  const params = new URLSearchParams(data).toString();
  try {
    const res = await fetch(`${apiBase}/scan?${params}`);
    const json = await res.json();
    renderTable(json.results);
  } catch (err) {
    alert("Error: " + err.message);
  }
});

function renderTable(arr) {
  const tbody = document.querySelector("#resultsTbl tbody");
  tbody.innerHTML = "";
  arr.forEach(row => {
    const tr = document.createElement("tr");
    tr.innerHTML = `<td>${row.symbol}</td><td>${row.price.toFixed(2)}</td><td>${row.pct_change_yoy.toFixed(2)}%</td>`;
    tbody.appendChild(tr);
  });
}