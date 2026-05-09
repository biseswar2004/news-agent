# summariser.py
# Sends articles to Gemini AI to write the spoken briefing script
# Falls back to Groq if Gemini fails

import google.generativeai as genai
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

# Setup Gemini (primary - free)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
gemini = genai.GenerativeModel("gemini-2.0-flash")
# Setup Groq (backup - free)
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def build_prompt(articles, name, topics):
    articles_text = ""
    for i, a in enumerate(articles[:20]):
        articles_text += f"\n{i+1}. [{a['source']}] {a['title']}\n"
        if a["summary"]:
            articles_text += f"   {a['summary'][:200]}\n"

    return f"""You are a personal news presenter for {name}.
Their interests: {', '.join(topics)}

Today's articles:
{articles_text}

Write a natural spoken morning briefing for {name}.
Rules:
- Start with: Good morning {name}!
- Sound like a smart friendly person talking
- Cover 6-8 stories, prioritise their interests
- Short sentences - this will be read aloud
- End with an energetic closing line
- NO bullet points, NO headers, NO markdown
- NO URLs or links mentioned
- Write ONLY the spoken words
- About 600 words total"""

def summarise_with_gemini(articles, name, topics):
    try:
        print("  🤖 Calling Gemini...")
        response = gemini.generate_content(build_prompt(articles, name, topics))
        script = response.text.strip()
        print(f"  ✓ Gemini done ({len(script)} chars)")
        return script
    except Exception as e:
        print(f"  ✗ Gemini failed: {e}")
        return None

def summarise_with_groq(articles, name, topics):
    try:
        print("  🤖 Trying Groq backup...")
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user",
                       "content": build_prompt(articles, name, topics)}],
            max_tokens=1000
        )
        script = response.choices[0].message.content.strip()
        print(f"  ✓ Groq done ({len(script)} chars)")
        return script
    except Exception as e:
        print(f"  ✗ Groq failed: {e}")
        return None

def generate_script(articles, name, topics):
    print("\n🧠 Generating script...")
    script = summarise_with_gemini(articles, name, topics)
    if not script:
        script = summarise_with_groq(articles, name, topics)
    if not script:
        print("  ⚠ Both AIs failed. Using headlines...")
        lines = [f"Good morning {name}! Here are today's headlines.\n"]
        for a in articles[:8]:
            lines.append(f"From {a['source']}: {a['title']}.")
        lines.append("\nHave a great day!")
        script = " ".join(lines)
    return script

# TEST - run: python summariser.py
if __name__ == "__main__":
    test_articles = [
        {"title": "India wins cricket match", "summary": "India beat Australia",
         "source": "ESPN", "link": ""},
        {"title": "Google releases new AI", "summary": "Gemini 2.0 launched",
         "source": "TechCrunch", "link": ""},
        {"title": "Startup raises 10 million", "summary": "Bangalore AI startup funded",
         "source": "YourStory", "link": ""},
    ]
    name = os.getenv("YOUR_NAME", "Friend")
    topics = os.getenv("YOUR_TOPICS", "AI,cricket").split(",")
    script = generate_script(test_articles, name, topics)
    print("\n--- SCRIPT ---")
    print(script[:500])
    print("\n✓ Summariser working!")