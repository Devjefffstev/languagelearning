import { NextRequest } from "next/server";

function convertContent(content: any): string {
  if (typeof content === "string") return content;
  if (Array.isArray(content)) {
    return content.map((c: any) => c.text || c.content || "").join("");
  }
  return String(content || "");
}

export async function POST(req: NextRequest) {
  try {
    const reqJson = await req.json();
    const { messages, systemPrompt, openUISystemPrompt } = reqJson;

    const finalSystemPrompt = openUISystemPrompt 
      ? `${systemPrompt}\n\n${openUISystemPrompt}` 
      : systemPrompt;

    console.log("\n========== OLLAMA REQUEST ==========");
    console.log("SYSTEM PROMPT:\n", finalSystemPrompt);
    console.log("\n--- FULL MESSAGES TO OLLAMA ---");
    console.log(JSON.stringify([
      { role: "system", content: finalSystemPrompt },
      ...messages.map((m: any) => ({
        role: m.role,
        content: typeof m.content === 'string' ? m.content : JSON.stringify(m.content)
      }))
    ], null, 2));
    console.log("======================================\n");

    const ollamaMessages = messages.map((m: any) => ({
      role: m.role,
      content: convertContent(m.content),
    }));

    const ollamaResponse = await fetch("http://localhost:11434/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        model: "gemma4:e2b",
        messages: [
          { role: "system", content: systemPrompt || "You are a professional AI assistant. Generate TWO distinct versions of your answer for each query. Present both options clearly labeled as 'Option 1' and 'Option 2'. Each option should be complete and ready to use. Maintain a professional tone throughout. Format your response so I can easily compare and choose between the two. When user provides data, always organize it in an OpenUI Lang Table component with clear columns and detailed information." },
          ...ollamaMessages,
        ],
        stream: true,
        options: {
          num_ctx: 131072,
        },
      }),
    });

    if (!ollamaResponse.ok) {
      throw new Error(`Ollama returned ${ollamaResponse.status}`);
    }

    const reader = ollamaResponse.body?.getReader();
    if (!reader) {
      throw new Error("No response body");
    }

    const stream = new ReadableStream({
      async start(controller) {
        const decoder = new TextDecoder();
        let buffer = "";
        let fullResponse = "";

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          buffer += decoder.decode(value, { stream: true });
          const lines = buffer.split("\n");
          buffer = lines.pop() || "";

          for (const line of lines) {
            if (!line.trim()) continue;
            try {
              const data = JSON.parse(line);
              if (data.message?.content) {
                fullResponse += data.message.content;
                const chunk = JSON.stringify({
                  choices: [{ delta: { content: data.message.content } }],
                });
                controller.enqueue(new TextEncoder().encode(chunk + "\n"));
              }
            } catch {}
          }
        }

        console.log("\n========== OLLAMA RESPONSE ==========");
    console.log(fullResponse);
    console.log("======================================\n");
        controller.close();
      },
    });

    return new Response(stream, {
      headers: {
        "Content-Type": "text/event-stream",
        "Cache-Control": "no-cache, no-transform",
        Connection: "keep-alive",
      },
    });
  } catch (err) {
    console.error("Ollama API error:", err);
    const message = err instanceof Error ? err.message : "Unknown error";
    return new Response(JSON.stringify({ error: message }), {
      status: 500,
      headers: { "Content-Type": "application/json" },
    });
  }
}