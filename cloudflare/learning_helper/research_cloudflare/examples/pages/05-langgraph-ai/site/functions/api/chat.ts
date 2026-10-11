// Pages Function: POST /api/chat
// Forwards the browser's message to the LangGraph agent (configured via the
// AGENT_URL environment variable) and returns the agent's reply.
//
// The ANTHROPIC_API_KEY lives only in the agent's process. The browser and
// this function never see it.
//
// Locally: set AGENT_URL in .dev.vars (see README).
// In production: set it under the Pages project's Settings -> Environment variables.

interface Env {
  AGENT_URL: string;
}

interface ChatRequest {
  message: string;
  thread_id?: string;
}

interface AgentReply {
  reply: string;
}

export const onRequestPost: PagesFunction<Env> = async (context) => {
  const { request, env } = context;

  if (!env.AGENT_URL) {
    return new Response(
      JSON.stringify({ error: "AGENT_URL is not configured on this Pages project." }),
      { status: 500, headers: { "content-type": "application/json" } },
    );
  }

  let body: ChatRequest;
  try {
    body = (await request.json()) as ChatRequest;
  } catch {
    return new Response(JSON.stringify({ error: "Invalid JSON body." }), {
      status: 400,
      headers: { "content-type": "application/json" },
    });
  }

  if (!body.message || typeof body.message !== "string" || !body.message.trim()) {
    return new Response(JSON.stringify({ error: "`message` must be a non-empty string." }), {
      status: 400,
      headers: { "content-type": "application/json" },
    });
  }

  try {
    const upstream = await fetch(env.AGENT_URL, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        message: body.message,
        thread_id: body.thread_id ?? "default-user",
      }),
    });

    const text = await upstream.text();
    let payload: AgentReply | { error: string };
    try {
      payload = JSON.parse(text);
    } catch {
      payload = { error: `Agent returned non-JSON: ${text.slice(0, 200)}` };
    }

    return new Response(JSON.stringify(payload), {
      status: upstream.ok ? 200 : upstream.status,
      headers: { "content-type": "application/json" },
    });
  } catch (err) {
    return new Response(
      JSON.stringify({ error: `Could not reach the agent: ${(err as Error).message}` }),
      { status: 502, headers: { "content-type": "application/json" } },
    );
  }
};

export const onRequestGet: PagesFunction<Env> = () =>
  new Response(JSON.stringify({ error: "Use POST." }), {
    status: 405,
    headers: { "content-type": "application/json", allow: "POST" },
  });