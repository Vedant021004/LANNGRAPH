from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel
import subprocess
import pyautogui
import pygetwindow as gw
import time

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-20b"
)


class State(BaseModel):
    question: str
    app: str = ""
    action: str = ""
    query: str = ""
    contact: str = ""
    message: str = ""
    answer: str = ""


def classifier(state: State):

    r = llm.invoke(
        f"""
        You are a desktop assistant.

        Understand what the user wants.

        Return ONLY this format:

        app|action|query|contact|message

        Apps:

        vscode
        spotify
        whatsapp
        chrome
        youtube
        github
        llm

        Actions:

        open
        search
        play
        pause
        next
        previous
        send_message
        none

        Examples:

        User: open vscode
        vscode|open|||

        User: open code
        vscode|open|||

        User: launch visual studio code
        vscode|open|||

        User: open spotify
        spotify|open|||

        User: play Spotify
        spotify|play|||

        User: resume Spotify
        spotify|play|||

        User: play Parvati on Spotify
        spotify|play|Parvati||

        User: pause Spotify
        spotify|pause|||

        User: pause the song
        spotify|pause|||

        User: next song
        spotify|next|||

        User: next track
        spotify|next|||

        User: skip this song
        spotify|next|||

        User: previous song
        spotify|previous|||

        User: previous track
        spotify|previous|||

        User: go back to the previous song
        spotify|previous|||

        User: open WhatsApp
        whatsapp|open|||

        User: send Rahul a message saying hello
        whatsapp|send_message||Rahul|hello

        User: message Rahul saying I will call you later
        whatsapp|send_message||Rahul|I will call you later

        User: send Mom a message saying I am coming home
        whatsapp|send_message||Mom|I am coming home

        User: open chrome
        chrome|open|||

        User: search LangGraph on Chrome
        chrome|search|LangGraph||

        User: open YouTube
        youtube|open|||

        User: play Python tutorial on YouTube
        youtube|play|Python tutorial||

        User: open GitHub
        github|open|||

        User: what is LangGraph?
        llm|none|||

        Return ONLY:

        app|action|query|contact|message

        User request:
        {state.question}
        """
    )

    result = r.content.strip()

    if "|" not in result:
        return {
            "app": "llm",
            "action": "none",
            "query": "",
            "contact": "",
            "message": ""
        }

    parts = result.split("|", 4)

    while len(parts) < 5:
        parts.append("")

    app = parts[0].strip().lower()
    action = parts[1].strip().lower()
    query = parts[2].strip()
    contact = parts[3].strip()
    message = parts[4].strip()

    return {
        "app": app,
        "action": action,
        "query": query,
        "contact": contact,
        "message": message
    }


def decide(state: State):

    if state.app == "vscode":
        return "vscode"

    if state.app == "spotify":
        return "spotify"

    if state.app == "whatsapp":
        return "whatsapp"

    if state.app == "chrome":
        return "chrome"

    if state.app == "youtube":
        return "youtube"

    if state.app == "github":
        return "github"

    return "general_llm"


def open_vscode(state: State):

    subprocess.Popen(
        ["code"]
    )

    return {
        "answer": "VS Code opened successfully."
    }


def open_spotify(state: State):

    if state.action == "open":

        subprocess.Popen(
            "start spotify:",
            shell=True
        )

        time.sleep(3)

        return {
            "answer": "Spotify opened successfully."
        }

    if state.action == "play":

        if state.query:

            subprocess.Popen(
                "start spotify:",
                shell=True
            )

            time.sleep(4)

            pyautogui.hotkey(
                "ctrl",
                "k"
            )

            time.sleep(1)

            pyautogui.write(
                state.query,
                interval=0.05
            )

            time.sleep(2)

            pyautogui.press(
                "enter"
            )

            time.sleep(3)

            pyautogui.press(
                "enter"
            )

            return {
                "answer": f"Playing {state.query} on Spotify."
            }

        pyautogui.press(
            "playpause"
        )

        return {
            "answer": "Spotify playback toggled."
        }

    if state.action == "pause":

        pyautogui.press(
            "playpause"
        )

        return {
            "answer": "Spotify playback toggled."
        }

    if state.action == "next":

        pyautogui.press(
            "nexttrack"
        )

        return {
            "answer": "Skipped to the next track."
        }

    if state.action == "previous":

        pyautogui.press(
            "prevtrack"
        )

        return {
            "answer": "Went back to the previous track."
        }

    return {
        "answer": "Spotify action not recognized."
    }


def focus_whatsapp():

    windows = gw.getWindowsWithTitle("WhatsApp")

    if not windows:
        return False

    whatsapp = windows[0]

    try:

        if whatsapp.isMinimized:
            whatsapp.restore()

        whatsapp.activate()

        time.sleep(2)

        pyautogui.click(
            whatsapp.left + whatsapp.width // 2,
            whatsapp.top + whatsapp.height // 2
        )

        time.sleep(1)

        return True

    except Exception:

        return False


def open_whatsapp(state: State):

    subprocess.Popen(
        "start whatsapp:",
        shell=True
    )

    time.sleep(5)

    if not focus_whatsapp():

        return {
            "answer": "WhatsApp Desktop was opened, but I could not focus the window."
        }

    if state.action == "open":

        return {
            "answer": "WhatsApp Desktop opened successfully."
        }

    if state.action == "send_message":

        print("\nWhatsApp Desktop")
        print("Contact:", state.contact)
        print("Message:", state.message)

        confirmation = input(
            "\nSend this message? (yes/no): "
        )

        if confirmation.lower().strip() != "yes":

            return {
                "answer": "Message cancelled."
            }

        if not focus_whatsapp():

            return {
                "answer": "Could not focus WhatsApp Desktop."
            }

        pyautogui.hotkey(
            "ctrl",
            "f"
        )

        time.sleep(1)

        pyautogui.write(
            state.contact,
            interval=0.05
        )

        time.sleep(2)

        pyautogui.press(
            "enter"
        )

        time.sleep(2)

        pyautogui.press(
            "enter"
        )

        time.sleep(2)

        pyautogui.write(
            state.message,
            interval=0.03
        )

        time.sleep(1)

        pyautogui.press(
            "enter"
        )

        time.sleep(2)

        return {
            "answer": f"Message sent to {state.contact}."
        }

    return {
        "answer": "WhatsApp Desktop opened successfully."
    }


def open_chrome(state: State):

    if state.action == "open":

        subprocess.Popen(
            [
                "cmd",
                "/c",
                "start",
                "",
                "chrome"
            ]
        )

        return {
            "answer": "Chrome opened successfully."
        }

    if state.action == "search":

        query = state.query.replace(
            " ",
            "+"
        )

        url = (
            f"https://www.google.com/search?q={query}"
        )

        subprocess.Popen(
            [
                "cmd",
                "/c",
                "start",
                "",
                "chrome",
                url
            ]
        )

        return {
            "answer": f"Searching Chrome for {state.query}."
        }

    return {
        "answer": "Chrome action not recognized."
    }


def open_youtube(state: State):

    if state.action == "open":

        subprocess.Popen(
            [
                "cmd",
                "/c",
                "start",
                "https://www.youtube.com"
            ]
        )

        return {
            "answer": "YouTube opened successfully."
        }

    if state.action in ["search", "play"]:

        query = state.query.replace(
            " ",
            "+"
        )

        url = (
            "https://www.youtube.com/results?search_query="
            + query
        )

        subprocess.Popen(
            [
                "cmd",
                "/c",
                "start",
                url
            ]
        )

        return {
            "answer": f"Searching YouTube for {state.query}."
        }

    return {
        "answer": "YouTube action not recognized."
    }


def open_github(state: State):

    subprocess.Popen(
        [
            "cmd",
            "/c",
            "start",
            "https://github.com/Vedant021004"
        ]
    )

    return {
        "answer": "GitHub opened successfully."
    }


def general_llm(state: State):

    r = llm.invoke(
        f"""
        You are a helpful AI assistant.

        Answer the user's question clearly,
        accurately and concisely.

        User question:
        {state.question}
        """
    )

    return {
        "answer": r.content
    }


graph = StateGraph(State)

graph.add_node(
    "classifier",
    classifier
)

graph.add_node(
    "vscode",
    open_vscode
)

graph.add_node(
    "spotify",
    open_spotify
)

graph.add_node(
    "whatsapp",
    open_whatsapp
)

graph.add_node(
    "chrome",
    open_chrome
)

graph.add_node(
    "youtube",
    open_youtube
)

graph.add_node(
    "github",
    open_github
)

graph.add_node(
    "general_llm",
    general_llm
)

graph.add_edge(
    START,
    "classifier"
)

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

graph.add_edge(
    "vscode",
    END
)

graph.add_edge(
    "spotify",
    END
)

graph.add_edge(
    "whatsapp",
    END
)

graph.add_edge(
    "chrome",
    END
)

graph.add_edge(
    "youtube",
    END
)

graph.add_edge(
    "github",
    END
)

graph.add_edge(
    "general_llm",
    END
)

app = graph.compile()


while True:

    question = input("\nAsk: ")

    if question.lower().strip() in [
        "exit",
        "quit",
        "q"
    ]:

        print("Goodbye!")

        break

    result = app.invoke(
        State(
            question=question
        )
    )

    print("\nApp:", result["app"])
    print("Action:", result["action"])
    print("Query:", result["query"])
    print("Contact:", result["contact"])
    print("Message:", result["message"])
    print("Answer:", result["answer"])