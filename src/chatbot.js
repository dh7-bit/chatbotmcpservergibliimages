import React, { useState, useRef, useEffect } from "react";

export default function Chatbot() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      type: "text",
      content: "Hello! Ask me anything 👋",
      loading: false
    }
  ]);

  const chatEndRef = useRef(null);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const isImagePrompt = (text) => {
    const lower = text.toLowerCase();
    return (
      lower.includes("ghibli") ||
      lower.includes("generate image") ||
      lower.includes("make image") ||
      lower.includes("create image") ||
      lower.includes("draw") ||
      lower.includes("photo")
    );
  };

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userText = input;
    const imageMode = isImagePrompt(userText);

    setMessages((prev) => [
      ...prev,
      { role: "user", type: "text", content: userText, loading: false },
      {
        role: "assistant",
        type: imageMode ? "image" : "text",
        content: "",
        image: "",
        loading: true
      }
    ]);

    setInput("");

    try {
      if (imageMode) {
        // IMAGE REQUEST
        const formData = new FormData();
        formData.append("message", userText);
        formData.append("type", "image");

        const response = await fetch("https://chatbotmcpservergibliimages.onrender.com/generate-image", {
          method: "POST",
          body: formData
        });

        const data = await response.json();

        setMessages((prev) => {
          const updated = [...prev];
          updated[updated.length - 1] = {
            role: "assistant",
            type: "image",
            content: data.caption || "Here is your generated image ✨",
            image: data.image_url,
            loading: false
          };
          return updated;
        });
      } else {
        // NORMAL TEXT CHAT (STREAMING)
        const response = await fetch("https://chatbotmcpservergibliimages.onrender.com/chat", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({ message: userText })
        });

        const reader = response.body.getReader();
        const decoder = new TextDecoder("utf-8");

        let fullText = "";

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          const chunkText = decoder.decode(value);
          const lines = chunkText.split("\n");

          for (let line of lines) {
            if (line.startsWith("data: ")) {
              const jsonStr = line.replace("data: ", "");
              if (!jsonStr.trim()) continue;

              try {
                const parsed = JSON.parse(jsonStr);

                if (parsed.chunk) {
                  fullText += parsed.chunk;

                  setMessages((prev) => {
                    const updated = [...prev];
                    updated[updated.length - 1] = {
                      role: "assistant",
                      type: "text",
                      content: fullText,
                      loading: false
                    };
                    return updated;
                  });
                }
              } catch (err) {
                console.error("JSON parse error:", err);
              }
            }
          }
        }
      }
    } catch (error) {
      console.error(error);

      setMessages((prev) => {
        const updated = [...prev];
        updated[updated.length - 1] = {
          role: "assistant",
          type: "text",
          content: "Error connecting to server.",
          loading: false
        };
        return updated;
      });
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center p-2 sm:p-4">
      <div className="w-full max-w-4xl h-[100dvh] sm:h-[92vh] bg-slate-900 text-white rounded-none sm:rounded-2xl shadow-2xl flex flex-col border border-slate-800 overflow-hidden">

        {/* Header */}
        <div className="px-4 py-4 sm:px-6 sm:py-5 border-b border-slate-700 shrink-0">
          <h1 className="text-xl sm:text-2xl font-bold">AI Chatbot</h1>
          <p className="text-slate-400 text-xs sm:text-sm mt-1">
            Chat + Ghibli Image Generator
          </p>
        </div>

        {/* Chat Area */}
        <div className="flex-1 overflow-y-auto px-3 py-4 sm:px-5 sm:py-5 space-y-4">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`flex ${
                msg.role === "user" ? "justify-end" : "justify-start"
              }`}
            >
              <div
                className={`max-w-[88%] sm:max-w-[75%] px-4 py-3 text-sm sm:text-base rounded-2xl whitespace-pre-wrap break-words leading-relaxed ${
                  msg.role === "user"
                    ? "bg-blue-600 text-white rounded-br-sm"
                    : "bg-slate-800 text-slate-100 rounded-bl-sm border border-slate-700"
                }`}
              >
                {/* TEXT MESSAGE */}
                {msg.type === "text" && (
                  <>
                    {msg.loading ? (
                      <span className="text-slate-400 animate-pulse">
                        Typing...
                      </span>
                    ) : (
                      <p>{msg.content}</p>
                    )}
                  </>
                )}

                {/* IMAGE MESSAGE */}
                {msg.type === "image" && (
                  <>
                    {msg.loading ? (
                      <span className="text-slate-400 animate-pulse">
                        Generating Image...
                      </span>
                    ) : (
                      <>
                        {msg.content && <p className="mb-2">{msg.content}</p>}
                        {msg.image && (
                          <img
                            src={msg.image}
                            alt="generated"
                            className="rounded-xl max-h-72 w-full object-cover"
                          />
                        )}
                      </>
                    )}
                  </>
                )}
              </div>
            </div>
          ))}
          <div ref={chatEndRef} />
        </div>

        {/* Input Area */}
        <div className="p-3 sm:p-4 border-t border-slate-700 bg-slate-900 shrink-0">
          <div className="flex flex-col sm:flex-row gap-3">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") sendMessage();
              }}
              placeholder="Type message or ask for Ghibli image..."
              className="flex-1 px-4 py-3 rounded-xl bg-slate-800 border border-slate-700 text-white placeholder:text-slate-400 outline-none focus:ring-2 focus:ring-blue-500 text-sm sm:text-base"
            />

            <button
              onClick={sendMessage}
              className="w-full sm:w-auto px-6 py-3 rounded-xl bg-blue-600 hover:bg-blue-500 transition font-semibold text-sm sm:text-base"
            >
              Send
            </button>
          </div>
        </div>

      </div>
    </div>
  );
}