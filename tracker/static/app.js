const API_URL = "http://127.0.0.1:8000";  // change if backend runs elsewhere
let token = null;

document.getElementById("login-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  try {
    const res = await fetch(`${API_URL}/login`, {
      method: "POST",
      headers: {"Content-Type": "application/x-www-form-urlencoded"},
      body: new URLSearchParams({username, password})
    });

    if (res.ok) {
      const data = await res.json();
      token = data.access_token;
      console.log("✅ Logged in. Token:", token);

      // Show app, hide login
      document.getElementById("login-section").style.display = "none";
      document.getElementById("app-section").style.display = "block";

      // Load expenses right after login
      await loadExpenses();
    } else {
      const errText = await res.text();
      console.error("❌ Login failed:", errText);
      alert("Login failed! " + errText);
    }
  } catch (err) {
    console.error("❌ Network error:", err);
    alert("Network error. Check backend is running.");
  }
});

// -----------------------------
// Handle Logout
// -----------------------------
document.getElementById("logout-btn").addEventListener("click", () => {
  token = null;
  document.getElementById("login-section").style.display = "block";
  document.getElementById("app-section").style.display = "none";
  console.log("👋 Logged out");
});

// -----------------------------
// Add Expense
// -----------------------------
document.getElementById("expense-form").addEventListener("submit", async (e) => {
  e.preventDefault();

  const amount = document.getElementById("amount").value;
  const category = document.getElementById("category").value;
  const description = document.getElementById("description").value;
  const dateValue = document.getElementById("date").value;

  // Ensure ISO date format
  const date = dateValue ? new Date(dateValue).toISOString() : new Date().toISOString();

  try {
    const res = await fetch(`${API_URL}/expenses/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      },
      body: JSON.stringify({ amount, category, description, date })
    });

    if (res.ok) {
      console.log("✅ Expense added");
      document.getElementById("expense-form").reset();
      await loadExpenses();
    } else {
      const errText = await res.text();
      console.error("❌ Error adding expense:", errText);
      alert("Error adding expense: " + errText);
    }
  } catch (err) {
    console.error("❌ Network error:", err);
    alert("Network error while adding expense");
  }
});

// -----------------------------
// Load Expenses
// -----------------------------
async function loadExpenses() {
  try {
    const res = await fetch(`${API_URL}/expenses/`, {
      headers: {"Authorization": `Bearer ${token}`}
    });

    if (res.ok) {
      const data = await res.json();
      console.log("📊 Loaded expenses:", data);

      const list = document.getElementById("expenses-list");
      list.innerHTML = "";

      data.forEach(exp => {
        const row = `<tr>
          <td>${exp.amount}</td>
          <td>${exp.category}</td>
          <td>${exp.description || ""}</td>
          <td>${new Date(exp.date).toLocaleDateString()}</td>
        </tr>`;
        list.innerHTML += row;
      });

      if (data.length === 0) {
        list.innerHTML = `<tr><td colspan="4">No expenses yet</td></tr>`;
      }

    } else {
      const errText = await res.text();
      console.error("❌ Failed to load expenses:", errText);
      alert("Error loading expenses: " + errText);
    }
  } catch (err) {
    console.error("❌ Network error while loading expenses:", err);
    alert("Network error while loading expenses");
  }
}
