const MAX_FIELD_LENGTH = 1200;

const readBody = async (req) => {
  if (req.body && typeof req.body === "object") {
    return req.body;
  }

  if (typeof req.body === "string") {
    return JSON.parse(req.body);
  }

  const chunks = [];

  for await (const chunk of req) {
    chunks.push(chunk);
  }

  if (!chunks.length) {
    return {};
  }

  return JSON.parse(Buffer.concat(chunks).toString("utf8"));
};

const clean = (value, maxLength = MAX_FIELD_LENGTH) =>
  String(value || "")
    .replace(/\s+/g, " ")
    .trim()
    .slice(0, maxLength);

const escapeHtml = (value) =>
  clean(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");

const getClientIp = (req) => {
  const forwarded = req.headers["x-forwarded-for"];

  if (typeof forwarded === "string" && forwarded.length > 0) {
    return forwarded.split(",")[0].trim();
  }

  return "unknown";
};

const sendJson = (res, statusCode, body) => {
  res.statusCode = statusCode;
  res.setHeader("Content-Type", "application/json; charset=utf-8");
  res.end(JSON.stringify(body));
};

module.exports = async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return sendJson(res, 405, { error: "Method not allowed." });
  }

  const token = process.env.TELEGRAM_BOT_TOKEN;
  const chatId = process.env.TELEGRAM_CHAT_ID;

  if (!token || !chatId) {
    return sendJson(res, 500, {
      error: "Telegram is not configured on this deployment.",
    });
  }

  let body;

  try {
    body = await readBody(req);
  } catch {
    return sendJson(res, 400, { error: "Invalid request body." });
  }

  const honeypot = clean(body.company, 120);

  if (honeypot) {
    return sendJson(res, 200, { ok: true });
  }

  const name = clean(body.name, 80);
  const contact = clean(body.contact, 120);
  const projectType = clean(body.projectType, 80);
  const budget = clean(body.budget, 80);
  const message = clean(body.message, MAX_FIELD_LENGTH);

  if (!name || !contact || !projectType || !message) {
    return sendJson(res, 400, { error: "Missing required fields." });
  }

  const submittedAt = new Date().toISOString();
  const ipAddress = getClientIp(req);

  const text = [
    "<b>New Cortex request</b>",
    "",
    `<b>Name:</b> ${escapeHtml(name)}`,
    `<b>Contact:</b> ${escapeHtml(contact)}`,
    `<b>Project:</b> ${escapeHtml(projectType)}`,
    `<b>Budget:</b> ${escapeHtml(budget || "Not decided")}`,
    "",
    `<b>Message:</b> ${escapeHtml(message)}`,
    "",
    `<b>Submitted:</b> ${escapeHtml(submittedAt)}`,
    `<b>IP:</b> ${escapeHtml(ipAddress)}`,
  ].join("\n");

  try {
    const telegramResponse = await fetch(
      `https://api.telegram.org/bot${token}/sendMessage`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          chat_id: chatId,
          text,
          parse_mode: "HTML",
          disable_web_page_preview: true,
        }),
      },
    );

    if (!telegramResponse.ok) {
      const errorText = await telegramResponse.text();
      console.error("Telegram API error", errorText);
      return sendJson(res, 502, { error: "Telegram rejected the message." });
    }

    return sendJson(res, 200, { ok: true });
  } catch (error) {
    console.error("Telegram delivery failed", error);
    return sendJson(res, 502, { error: "Telegram delivery failed." });
  }
};
