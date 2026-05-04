const form = document.querySelector("#request-form");
const statusEl = document.querySelector("#form-status");
const submitButton = form?.querySelector("button[type='submit']");

const setStatus = (message, type = "") => {
  statusEl.textContent = message;
  statusEl.className = `form-status${type ? ` is-${type}` : ""}`;
};

const getPayload = () => {
  const data = new FormData(form);

  return {
    name: data.get("name")?.toString().trim() || "",
    contact: data.get("contact")?.toString().trim() || "",
    projectType: data.get("projectType")?.toString().trim() || "",
    budget: data.get("budget")?.toString().trim() || "",
    message: data.get("message")?.toString().trim() || "",
    company: data.get("company")?.toString().trim() || "",
  };
};

form?.addEventListener("submit", async (event) => {
  event.preventDefault();
  setStatus("");

  if (!form.reportValidity()) {
    setStatus("Please complete the required fields.", "error");
    return;
  }

  const payload = getPayload();

  submitButton.disabled = true;
  setStatus("Sending request...");

  try {
    const response = await fetch("/api/telegram", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    const result = await response.json().catch(() => ({}));

    if (!response.ok) {
      throw new Error(result.error || "Telegram delivery failed.");
    }

    form.reset();
    setStatus("Sent. The request is now in Telegram.", "success");
  } catch (error) {
    setStatus(error.message || "Something went wrong. Please try again.", "error");
  } finally {
    submitButton.disabled = false;
  }
});
