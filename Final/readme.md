# How to Turn Your Python Project into a Website!

This guide helps you take your Python program (like `my_chatbot.py`) and make it into a **website** using Flask.

---

### Why Do This?

* **Before:** You had to type in the console.
* **Now:** You can use your program in a **web browser**. It’s cleaner and more fun!

---

## 1. Open PyCharm

* Find **PyCharm** on your computer and open it.
* Wait until your project loads.

---

## 2. Create a New Folder for the Web Version

1. On the **left panel** (Project), find your current folder that has `my_chatbot.py`.
2. **Right-click** on the folder or in empty space.
3. Select **New → Directory (or Folder)**.
4. Name it:

   ```
   web_version
   ```
5. Press **Enter**.

Now you have a **new folder** called `web_version`.

---

## 3. Create a New Python File

1. **Right-click** on `web_version`.
2. Select **New → Python File**.
3. Name it:

   ```
   app.py
   ```
4. Press **Enter**.
   This will be the program for your website.

---

## 4. Get Example Code from GitHub

1. Open this link:
   **[https://github.com/luomi16/idtech/tree/main/Final](https://github.com/luomi16/idtech/tree/main/Final)**
2. Click the file called **improved.py**.
3. Click **Raw** (button near the top right).
4. **Copy all the text**:

   * Windows: **Ctrl+A**, then **Ctrl+C**
   * Mac: **Command+A**, then **Command+C**

---

## 5. Paste Code into `app.py`

1. Go back to **PyCharm**.
2. Click inside `app.py`.
3. Paste:

   * Windows: **Ctrl+V**

---

## 6. Edit the Code for Your Own Program

1. **API Key**
   On **line 9**, change:

   ```python
   api_key="your_api_key_here"
   ```

   to your own API key.

2. **Change Assistant Details**
   From around **line 19**, you will see code that creates the assistant:

   ```python
   ai_assistant = client.beta.assistants.create(
       name="Restaurant Advisor",
       instructions="You help find restaurants.",
       model="gpt-3.5-turbo",
       tools=[{"type": "file_search"}]
   )
   ```

   Change **name** and **instructions** to match your program.

3. **HTML Template**

   * In `web_version`, **right-click** → New → Directory → name it **templates**
   * Right-click `templates` → New → HTML File → name it **index.html**
   * Go back to the GitHub folder and open **index.html** (inside `templates`).
   * Copy everything and paste into your new `index.html`.

---

## 7. Install Flask (Do This Once)

1. At the bottom of PyCharm, click **Terminal**.

2. Type:

   ```
   pip install flask openai
   ```

3. Press **Enter** and wait.

---

## 8. Run Your Website

1. Open `app.py`.
2. Click the green **Run button** (triangle).
3. Look at the output for:

   ```
   Running on http://127.0.0.1:5000/
   ```
4. Hold **Ctrl (Windows)** or **Command (Mac)** and click the link.
   A browser window will open with your chatbot website!

---

## 9. Test Your Website

* Type something into the input box.
* Click **Submit**.
* Your chatbot will respond on the web page.

---

## 10. Tips

* If you break your code, you can always **recopy from GitHub**.
* Keep your **old file** (`my_chatbot.py`) as backup.
* Press the **reload** button on your browser if the page looks stuck.

---


