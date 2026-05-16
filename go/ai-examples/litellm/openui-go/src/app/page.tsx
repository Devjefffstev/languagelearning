"use client";
import "@openuidev/react-ui/components.css";
import "@openuidev/react-ui/styles/index.css";

import { FullScreen } from "@openuidev/react-ui";
import { openAIMessageFormat, openAIReadableStreamAdapter } from "@openuidev/react-headless";
import { openuiLibrary, openuiPromptOptions } from "@openuidev/react-ui/genui-lib";

const systemPrompt = openuiLibrary.prompt({
  ...openuiPromptOptions,
  additionalRules: [
    "Generate UI using OpenUI Lang syntax ONLY.",
    "Format: root = ComponentName([props], [...children])",
    "Examples: root = Card([TextContent('Title', 'large')])",
    "DO NOT use markdown code blocks. Use OpenUI Lang directly.",
  ],
  preamble: "You are a UI generator. Always respond with OpenUI Lang code that can be rendered as React components.",
});

const customSystemPrompt = "You are a customer support assistant. ALWAYS generate TWO answer options labeled 'Option 1' and 'Option 2'. Table syntax: Table([Col('label', data)]) - ONE arg only. Output: root = Stack([table, card]) table = Table([Col('Field', F), Col('Value', V)]) card = Card([TextContent('Option 1: [answer1]'), TextContent('Option 2: [answer2]')], 'column'). F=['Name','ID','Wallet','Question'], V=[extracted from user]. Example: root=S([t,c]) t=T([C('F',['N']),C('V',['Jeff'])]) c=C([Tx('Opt1: call'),Tx('Opt2: email')],'column')";

export default function Home() {
  return (
    <div className="h-screen w-screen overflow-hidden" key="openui-chat">
      <FullScreen
        apiUrl="/api/ollama"
        processMessage={async ({ messages, abortController }) => {
          return fetch("/api/ollama", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              systemPrompt: customSystemPrompt,
              messages: openAIMessageFormat.toApi(messages),
            }),
            signal: abortController.signal,
          });
        }}
        streamProtocol={openAIReadableStreamAdapter()}
        messageFormat={openAIMessageFormat}
        componentLibrary={openuiLibrary}
        agentName="OpenUI Chat"
        welcomeMessage={{
          title: "Hello! 👋",
          description: "Ask me anything about the weather or anything else.",
        }}
        conversationStarters={{
          options: [
               { displayText: "user: Jeff Soto id: 232344 wallet: isx045332", prompt: "user: Jeff Soto id: 232344 wallet: isx045332. the client has the following question: my desposit was not received. " },
            { displayText: "user: Nadia Soto id: 232344 wallet: isx045332", prompt: "user: Nadia Soto id: 232344 wallet: isx045332. the client has the following question: how to check my account balance. " },
            { displayText: "user: Nat Lug id: 232344 wallet: isx045332", prompt: "user: Nat Lug id: 232344 wallet: isx045332. the client has the following question: I tried to request a loan but my request was denied. " },
          ],
        }}
      />
    </div>
  );
}
