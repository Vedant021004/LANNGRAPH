Absolutely — for this project, the README should explain **what the agent does, why LangGraph is used, how the classifier works, how each node works, and how the complete request flows**.

Here’s a clean, beginner-friendly but professional README you can put directly in `README.md`:

````markdown
# 🖥️ LangGraph Desktop AI Assistant

An AI-powered desktop assistant built with **LangGraph, Groq, Python, and PyAutoGUI** that understands natural-language commands and performs actions on desktop applications.

Instead of building separate commands such as:

```text
"open chrome"
"next song"
"send Rahul hello"
````

the assistant uses an LLM to understand the user's request, convert it into a structured action, and then LangGraph routes that action to the correct application node.

---

## 🚀 What Can It Do?

The assistant currently supports:

| Application         | Supported Actions                 |
| ------------------- | --------------------------------- |
| 🎵 Spotify          | Open, Play, Pause, Next, Previous |
| 💬 WhatsApp Desktop | Open, Send Message                |
| 🌐 Chrome           | Open, Google Search               |
| ▶️ YouTube          | Open, Search, Play                |
| 💻 VS Code          | Open                              |
| 🐙 GitHub           | Open                              |
| 🤖 General LLM      | Answer normal questions           |

Examples:

```text
open spotify

pause spotify

next song

previous song

play Parvati on Spotify

open WhatsApp

send Rahul a message saying hello

search LangGraph on Chrome

play Python tutorial on YouTube

open vscode

open github

what is LangGraph?
```

---

# 🧠 Architecture

The assistant follows a simple **classify → route → execute** architecture.

```text
                         USER
                           │
                           ▼
                  Natural Language
                           │
                           ▼
                  ┌─────────────────┐
                  │   Groq LLM      │
                  │   Classifier    │
                  └────────┬────────┘
                           │
                           ▼
              Structured Action Format
              app|action|query|contact|message
                           │
                           ▼
                  ┌─────────────────┐
                  │    LangGraph    │
                  │     Router      │
                  └────────┬────────┘
                           │
          ┌────────────────┼─────────────────┐
          │                │                 │
          ▼                ▼                 ▼
      Spotify          WhatsApp          Chrome
          │                │                 │
          ▼                ▼                 ▼
      PyAutoGUI        PyAutoGUI        Subprocess
          │                │                 │
          ▼                ▼                 ▼
     Spotify App      WhatsApp App       Chrome
```

The important idea is:

> **The LLM decides what the user wants. LangGraph decides where the request should go. Python performs the actual action.**

---

# 🔄 How a Request Works

Suppose the user says:

```text
next song
```

### Step 1 — User Input

The program receives:

```text
next song
```

---

### Step 2 — LLM Classification

The request is sent to Groq.

The classifier converts the natural-language request into:

```text
spotify|next|||
```

The format is:

```text
app|action|query|contact|message
```

So:

```text
spotify
```

means the request belongs to Spotify.

```text
next
```

means the requested action is the next track.

---

### Step 3 — LangGraph Routing

LangGraph receives the classification.

The graph checks:

```python
if state.app == "spotify":
    return "spotify"
```

The request is therefore routed to:

```text
Spotify Node
```

---

### Step 4 — Execute the Action

The Spotify node executes:

```python
pyautogui.press("nexttrack")
```

Windows receives the media-key command.

Spotify then moves to the next track.

---

### Step 5 — Response

The assistant returns:

```text
Skipped to the next track.
```

---

# 🏗️ LangGraph Architecture

The graph contains several nodes.

```text
START
  │
  ▼
Classifier
  │
  ├──────► VS Code
  │
  ├──────► Spotify
  │
  ├──────► WhatsApp
  │
  ├──────► Chrome
  │
  ├──────► YouTube
  │
  ├──────► GitHub
  │
  └──────► General LLM
                 │
                 ▼
                END
```

The graph starts at:

```text
START
```

and always goes through:

```text
Classifier
```

The classifier determines which application should handle the request.

Then LangGraph uses conditional routing:

```python
graph.add_conditional_edges(
    "classifier",
    decide,
    {
        "vscode": "vscode",
        "spotify": "spotify",
        "whatsapp": "whatsapp",
        "chrome": "chrome",
        "youtube": "youtube",
        "github": "github",
        "general_llm": "general_llm"
    }
)
```

After the application node finishes:

```text
Application Node
      ↓
     END
```

---

# 🧩 State

The entire workflow shares a common state.

```python
class State(BaseModel):

    question: str

    app: str = ""

    action: str = ""

    query: str = ""

    contact: str = ""

    message: str = ""

    answer: str = ""
```

The state acts as the **shared memory of the current request**.

For example:

```text
question:
"send Rahul a message saying hello"

app:
"whatsapp"

action:
"send_message"

query:
""

contact:
"Rahul"

message:
"hello"
```

This allows different nodes in the graph to access the information they need.

---

# 🧠 Why Use an LLM Classifier?

A traditional command system might require:

```python
if "spotify" in question:
    ...
```

and:

```python
if "next song" in question:
    ...
```

This becomes difficult when users phrase the same request differently.

For example:

```text
next song

skip this song

play the next track

go to the next track

move to the next song
```

All of these mean approximately the same thing.

The LLM allows the user to speak naturally.

The classifier converts the different expressions into the same structured action:

```text
spotify|next|||
```

---

# 📦 Structured Output

Instead of asking the LLM to generate a long response, the classifier is instructed to return:

```text
app|action|query|contact|message
```

Example:

```text
play Parvati on Spotify
```

becomes:

```text
spotify|play|Parvati||
```

Another example:

```text
send Rahul a message saying I will call you later
```

becomes:

```text
whatsapp|send_message||Rahul|I will call you later
```

The Python program then splits the result:

```python
parts = result.split("|", 4)
```

This gives:

```text
parts[0] → app
parts[1] → action
parts[2] → query
parts[3] → contact
parts[4] → message
```

---

# 🎵 Spotify

Spotify is controlled using Windows media commands.

### Open Spotify

```python
subprocess.Popen(
    "start spotify:",
    shell=True
)
```

### Play / Pause

```python
pyautogui.press("playpause")
```

This sends the system Play/Pause media command.

### Next Track

```python
pyautogui.press("nexttrack")
```

### Previous Track

```python
pyautogui.press("prevtrack")
```

The architecture is:

```text
User
 │
 ▼
"next song"
 │
 ▼
Groq
 │
 ▼
spotify|next|||
 │
 ▼
LangGraph
 │
 ▼
Spotify Node
 │
 ▼
PyAutoGUI
 │
 ▼
Windows Media Key
 │
 ▼
Spotify Desktop
```

### Important

`playpause` is a toggle.

Therefore:

```text
play → playpause
pause → playpause
```

depends on the current Spotify playback state.

---

# 💬 WhatsApp Desktop

The project uses **WhatsApp Desktop**, not WhatsApp Web.

The workflow uses:

```text
subprocess
     ↓
Open WhatsApp Desktop
     ↓
pygetwindow
     ↓
Find WhatsApp window
     ↓
Activate WhatsApp
     ↓
PyAutoGUI
     ↓
Keyboard interaction
```

### Why `pygetwindow`?

PyAutoGUI controls the keyboard and mouse, but the correct application must be focused first.

`pygetwindow` finds the WhatsApp window:

```python
windows = gw.getWindowsWithTitle("WhatsApp")
```

Then the application is activated:

```python
whatsapp.activate()
```

This prevents keyboard commands from accidentally going to another application such as VS Code.

### Sending a Message

Example:

```text
send Rahul a message saying hello
```

Classifier:

```text
whatsapp|send_message||Rahul|hello
```

Then the WhatsApp node:

1. Opens WhatsApp Desktop.
2. Finds the WhatsApp window.
3. Activates it.
4. Asks the user for confirmation.
5. Opens search.
6. Searches for the contact.
7. Opens the chat.
8. Types the message.
9. Presses Enter.

The confirmation step is intentional:

```text
Send this message? (yes/no):
```

This prevents accidental messages from being sent.

---

# 🌐 Chrome

Chrome supports:

```text
open chrome
```

and:

```text
search LangGraph on Chrome
```

The classifier produces:

```text
chrome|search|LangGraph||
```

The Chrome node then creates a Google search URL and launches Chrome.

Architecture:

```text
User
 ↓
Groq
 ↓
chrome|search|LangGraph||
 ↓
LangGraph
 ↓
Chrome Node
 ↓
subprocess
 ↓
Chrome
```

---

# ▶️ YouTube

YouTube supports:

```text
open YouTube
```

and:

```text
play Python tutorial on YouTube
```

The second command becomes:

```text
youtube|play|Python tutorial||
```

The application opens YouTube search results for the requested query.

---

# 💻 VS Code

VS Code is launched using:

```python
subprocess.Popen(
    ["code"]
)
```

Example:

```text
open vscode
```

becomes:

```text
vscode|open|||
```

and gets routed to the VS Code node.

---

# 🐙 GitHub

GitHub is opened through the Windows command:

```python
subprocess.Popen(
    [
        "cmd",
        "/c",
        "start",
        "https://github.com"
    ]
)
```

Example:

```text
open github
```

becomes:

```text
github|open|||
```

---

# 🤖 General LLM

Not every request is a desktop command.

For example:

```text
What is LangGraph?
```

The classifier returns:

```text
llm|none|||
```

LangGraph routes it to:

```text
general_llm
```

The LLM then answers normally.

This gives the assistant two capabilities:

```text
Desktop Automation
        +
General AI Assistant
```

---

# 🛠️ Technologies Used

| Technology    | Purpose                     |
| ------------- | --------------------------- |
| Python        | Core application            |
| LangGraph     | Workflow and routing        |
| LangChain     | LLM integration             |
| Groq          | Fast LLM inference          |
| Pydantic      | State structure             |
| PyAutoGUI     | Keyboard/mouse automation   |
| PyGetWindow   | Window detection/focus      |
| Subprocess    | Launch desktop applications |
| python-dotenv | Environment variables       |

---

# 📁 Project Structure

```text
desktop-ai-assistant/
│
├── main.py
│
├── .env
│
├── requirements.txt
│
└── README.md
```

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone <your-repository-url>
cd desktop-ai-assistant
```

## 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

## 3. Install dependencies

```bash
pip install langchain-groq langgraph pydantic python-dotenv pyautogui pygetwindow
```

## 4. Add your Groq API key

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

---

# ▶️ Run the Assistant

```bash
python main.py
```

You will see:

```text
Ask:
```

Now enter commands such as:

```text
Ask: open spotify
```

or:

```text
Ask: next song
```

or:

```text
Ask: search LangGraph on Chrome
```

or:

```text
Ask: what is LangGraph?
```

To exit:

```text
exit
```

---

# 🔐 Safety

Some actions interact directly with desktop applications.

For example:

```text
WhatsApp → sending a message
```

The assistant therefore asks for confirmation before sending:

```text
Send this message? (yes/no):
```

This is important because an AI classifier should not blindly perform consequential actions.

---

# ⚠️ Current Limitations

This project currently uses desktop/UI automation, so some actions depend on the application's current UI.

### WhatsApp

PyAutoGUI relies on keyboard interaction and therefore can be affected by:

* UI changes
* Window focus
* Loading delays
* Different WhatsApp Desktop versions

### Spotify

The media-key approach uses:

```text
Play/Pause
Next
Previous
```

It does not directly query Spotify's playback state.

### YouTube

The current implementation searches YouTube rather than guaranteeing that the exact requested video automatically starts playing.

### LLM Classification

The classifier relies on the LLM following the required format:

```text
app|action|query|contact|message
```

Production versions should use stronger structured validation.

---

# 🔮 Future Improvements

This project is designed to grow into a more capable **AI desktop agent**.

Possible improvements include:

```text
Current
│
├── LLM Classification
├── LangGraph Routing
├── Desktop Automation
└── Application Actions
        │
        ▼
Future
│
├── Voice Input
│
├── Speech-to-Text
│
├── Better Intent Classification
│
├── Tool Calling
│
├── Memory
│
├── Multi-step Tasks
│
├── Application State Detection
│
├── Windows UI Automation
│
└── Agent Planning
```

Possible future commands:

```text
"Open Spotify and play my workout playlist"

"Send Rahul the file I downloaded"

"Search Google and summarize the first three results"

"Open VS Code and run my project"

"Play the next song and lower the volume"

"Open GitHub and check my notifications"
```

---

# 🧠 Core Design Philosophy

The main idea of this project is to separate **understanding, routing, and execution**.

```text
┌──────────────────────┐
│      UNDERSTAND      │
│                      │
│       Groq LLM       │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│        ROUTE         │
│                      │
│      LangGraph       │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│       EXECUTE        │
│                      │
│ Python / PyAutoGUI   │
│ Subprocess / Apps    │
└──────────────────────┘
```

The LLM does **not** directly control the computer.

Instead:

```text
LLM
 ↓
Structured Intent
 ↓
LangGraph
 ↓
Controlled Python Function
 ↓
Desktop Application
```

This makes the system easier to understand, debug, and extend.

---

# ⭐ Why LangGraph?

LangGraph is useful here because the assistant is not just a chatbot.

It is a workflow:

```text
Input
 ↓
Classification
 ↓
Decision
 ↓
Application-specific action
 ↓
Result
```

Each application can be represented as an independent node.

Adding a new application therefore becomes easier:

```text
New App
   ↓
Create Node
   ↓
Add Classifier Instructions
   ↓
Add Router
   ↓
Connect Node → END
```

For example, a future Discord node could follow:

```text
User
 ↓
Groq
 ↓
discord|send_message||Rahul|Hello
 ↓
LangGraph
 ↓
Discord Node
 ↓
Desktop Automation
```

---

# 📊 Example End-to-End Requests

### Spotify

```text
User:
"next song"

        ↓

Groq:
spotify|next|||

        ↓

LangGraph:
Spotify Node

        ↓

PyAutoGUI:
nexttrack

        ↓

Spotify:
Next Track
```

### WhatsApp

```text
User:
"send Rahul a message saying I'll call you later"

        ↓

Groq:
whatsapp|send_message||Rahul|I'll call you later

        ↓

LangGraph:
WhatsApp Node

        ↓

Confirmation

        ↓

PyAutoGUI

        ↓

WhatsApp Desktop
```

### Chrome

```text
User:
"search LangGraph on Chrome"

        ↓

Groq:
chrome|search|LangGraph||

        ↓

LangGraph:
Chrome Node

        ↓

Subprocess

        ↓

Chrome + Google Search
```

### General Question

```text
User:
"What is LangGraph?"

        ↓

Groq:
llm|none|||

        ↓

LangGraph:
General LLM Node

        ↓

LLM Response
```

---

# 🎯 Project Goal

The goal of this project is to build a foundation for a **natural-language desktop agent**.

Instead of remembering application-specific commands, the user can communicate naturally:

```text
"open Spotify"

"skip this song"

"send Rahul a message"

"search this on Chrome"

"open my GitHub"

"what is LangGraph?"
```

The system translates these requests into structured actions and uses **LangGraph as the orchestration layer** to execute the correct workflow.

---

## 👨‍💻 Author

**Vedant**

Built as a practical exploration of:

* Generative AI
* LLM-based intent classification
* LangGraph
* Agentic workflows
* Desktop automation
* Tool-based AI systems
* Human-in-the-loop execution

---

## 📜 License

This project is for educational and experimental purposes.

```

### One architecture point I especially recommend keeping

This sentence makes the project immediately understandable to someone reviewing your GitHub:

> **“The LLM decides what the user wants. LangGraph decides where the request should go. Python performs the actual action.”**

That gives a new contributor/reviewer the entire mental model in one line.
```
