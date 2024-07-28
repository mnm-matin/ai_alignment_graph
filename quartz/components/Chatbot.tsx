import { QuartzComponentConstructor, QuartzComponentProps } from "./types"
import chatbotStyle from "./styles/chatbot.scss"

interface Options {
  placeholder?: string
  buttonText?: string
  maxMessages?: number
}

const defaultOptions: Options = {
  placeholder: "Type a message...",
  buttonText: "Send",
  maxMessages: 50
}

export default ((userOpts?: Partial<Options>) => {
  const opts = { ...defaultOptions, ...userOpts }
  
  function Chatbot(props: QuartzComponentProps) {
    return (
      <div class="chatbot">
        <div class="chat-messages" id="chat-messages">
          {/* Messages will be dynamically added here */}
        </div>
        <form id="chatbot-form">
          <input
            type="text"
            id="chatbot-input"
            placeholder={opts.placeholder}
          />
          <button type="submit">{opts.buttonText}</button>
        </form>
      </div>
    )
  }

  Chatbot.css = chatbotStyle

  Chatbot.afterDOMLoaded = `
    const form = document.getElementById('chatbot-form');
    const input = document.getElementById('chatbot-input');
    const messagesContainer = document.getElementById('chat-messages');
    let messages = [];

    function addMessage(text, sender) {
      messages.push({ text, sender });
      if (messages.length > ${opts.maxMessages}) {
        messages.shift();
      }
      renderMessages();
    }

    function renderMessages() {
      messagesContainer.innerHTML = messages.map(msg => 
        \`<div class="message \${msg.sender}">\${msg.text}</div>\`
      ).join('');
      messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const text = input.value.trim();
      if (text) {
        addMessage(text, 'user');
        input.value = '';
        
        // Simulate bot response
        setTimeout(() => {
          addMessage(\`You said: \${text}\`, 'bot');
        }, 1000);
      }
    });
  `

  return Chatbot
}) satisfies QuartzComponentConstructor