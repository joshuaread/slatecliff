document.getElementById("y").textContent = new Date().getFullYear();

function qs(name) {
  return new URLSearchParams(location.search).get(name);
}

async function submitWaitlist(form) {
  const status = document.getElementById("form-status");
  const email = (form.email && form.email.value || "").trim();
  const firm = (form.firm && form.firm.value || "").trim();
  const pain = (form.pain && form.pain.value || "").trim();
  if (!email) return;

  const key = (window.SLATECLIFF && window.SLATECLIFF.web3formsAccessKey) || "";
  const btn = form.querySelector('button[type="submit"]');
  if (btn) btn.disabled = true;

  if (!key) {
    // Capture not wired yet — still route to thanks so the door feels real while key is added.
    const params = new URLSearchParams({ email });
    if (firm) params.set("firm", firm);
    if (pain) params.set("pain", pain);
    location.href = "thanks.html?" + params.toString();
    return;
  }

  try {
    if (status) status.textContent = "Sending…";
    const res = await fetch("https://api.web3forms.com/submit", {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify({
        access_key: key,
        subject: (window.SLATECLIFF && window.SLATECLIFF.formSubject) || "Slatecliff beta signup",
        from_name: (window.SLATECLIFF && window.SLATECLIFF.fromName) || "Slatecliff Waitlist",
        email,
        firm: firm || "(none)",
        pain: pain || "(not provided)",
        page: location.href
      })
    });
    const data = await res.json();
    if (!res.ok || data.success === false) throw new Error(data.message || "Submit failed");
    location.href = "thanks.html";
  } catch (err) {
    if (status) status.textContent = "Something went wrong — email hello@slatecliff.com or try again.";
    if (btn) btn.disabled = false;
    console.error(err);
  }
}

document.querySelectorAll("form.signup").forEach((form) => {
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    submitWaitlist(form);
  });
});

// Prefill thanks page if query params present (optional)
if (location.pathname.endsWith("thanks.html") && qs("email")) {
  /* no-op; kept for analytics hooks later */
}