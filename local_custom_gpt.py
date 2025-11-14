import ollama
from docx import Document
from PyPDF2 import PdfReader
import os
import re

# adjust prompt as you see fit
SYSTEM_PROMPT = """
You are a Study Assistant, an AI assistant that helps students stay organized, plan homework, and study efficiently.

Rules:
- Be proactive, helpful, and concise.
- Ask clarifying questions when needed.
- Tell explicit instructions if you require a user to do something additionl.
"""

def extract_file_text(filepath):
    ext = filepath.lower().split(".")[-1]

    if ext == "txt":
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()

    elif ext == "pdf":
        reader = PdfReader(filepath)
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    elif ext == "docx":
        doc = Document(filepath)
        return "\n".join(p.text for p in doc.paragraphs)

    return None


def main():
    print("\n===== Study Assistant =====")
    print("Type your prompt. Add `file <path>` anywhere to attach a file.")
    print("Example: summarize this chapter. file notes.pdf\n")

    history = [{"role": "system", "content": SYSTEM_PROMPT}]

    file_pattern = re.compile(r"file\s+(.+)", re.IGNORECASE)

    while True:
        try:
            user_input = input("🟢 You: ")

            if user_input.lower() == "exit":
                print("\n👋 Goodbye")
                break

            # Check for file mention in the prompt
            match = file_pattern.search(user_input)
            if match:
                filepath = match.group(1).strip()

                if os.path.exists(filepath):
                    print("📄 Reading file...")
                    file_text = extract_file_text(filepath)
                    if file_text:
                        # Remove the file command from message
                        prompt_without_file = file_pattern.sub("", user_input).strip()

                        # Build combined user prompt
                        user_input = (
                            f"{prompt_without_file}\n\n"
                            f"Here is the file content:\n\n"
                            f"{file_text}"
                        )
                    else:
                        print("❌ Unsupported file type.\n")
                        continue
                else:
                    print("❌ File not found.\n")
                    continue

            history.append({"role": "user", "content": user_input})

            response = ollama.chat(
                model="llama3.1",  # change to whichever model you use
                messages=history,
            )

            reply = response["message"]["content"]
            print(f"\n🤖 Study Assistant:\n{reply}\n")

            history.append({"role": "assistant", "content": reply})

        except KeyboardInterrupt:
            print("\n👋 Goodbye")
            break


if __name__ == "__main__":
    main()
