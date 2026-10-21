# TA Live Demo Script — Python for APIs and GenAI Integration
> Session 33 | Runtime: ~7 minutes | Delivered at session end, after Balaji's lecture

**Setup before class starts:** A notebook with the requests library installed, OPENAI_API_KEY already set as an environment variable before class (never shown on screen), the model name from the instructor, and a saved sample response in a cell as a backup if the network or key fails.

---

```
STEP 1 — Make a first request (≈1 min)
  Action: Type and run: response = requests.get("https://jsonplaceholder.typicode.com/todos/1") then print(response.status_code) and print(response.json()).
  Result: 200, then a small dictionary
  Say out loud: "This is the waiter taking our order to the kitchen. The answer comes back as a dictionary, which we met in 14.1."
```

```
STEP 2 — Check the status (≈1 min)
  Action: Request .../todos/99999 and print the status code.
  Result: 404
  Say out loud: "Always check the status before you use the answer. 404 means address not found."
```

```
STEP 3 — Send a prompt to GenAI (≈3 min)
  Action: Show the headers with the key read from os.environ and the body with a system message and a user message: "Summarise in 3 sentences: Pune's revenue grew 9% this month, slower than Bengaluru's 12%, but ahead of Chennai's -3%." Run requests.post(url, headers=headers, json=body, timeout=60) and print data["choices"][0]["message"]["content"].
  Result: A short summary in the printed output
  Say out loud: "Read the path left to right: choices, the first item, message, content. That is where the answer lives in the response."
```

```
STEP 4 — Keep it safe and check it (≈2 min)
  Action: Point at the os.environ line and say what would happen if the key were pasted into shared code. Then check the summary's numbers against the prompt.
  Result: The numbers match the prompt
  Say out loud: "The key is a password and a card number in one. Keep it out of the code. And a GenAI reply still needs checking, exactly like in the workflow sessions."
```

---

> **TA TALKING POINT:** "An API call is just a request with a key. Keep the key out of the code, check the status, and still check the answer."
